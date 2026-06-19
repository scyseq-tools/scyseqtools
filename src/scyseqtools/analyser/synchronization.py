"""
Synchronization likelihood and direction support for the analyser GUI.
"""

import csv
import io
import os
import pathlib
import tkinter
import tkinter.filedialog
import tkinter.messagebox

import numpy as np
import Pmw

from scyseq.information import mutual_information
from scyseq.recurrence import mcr, synchronization_likelihood


TABLE_EXT = ".csv"
SEP = ";"
OUTPUT_DIR = "synchronization_likelihood_direction"


def _sequence_values(sequence):
    return np.asarray(getattr(sequence, "ivals", sequence), dtype=int)


def _alphabet_labels(sequence):
    alphabet = getattr(sequence, "alphabet", None)
    if alphabet is None:
        return ()
    if hasattr(alphabet, "svals"):
        return tuple(alphabet.svals)
    return tuple(getattr(sym, "sval", getattr(sym, "strval", str(sym)))
                 for sym in alphabet)


def common_sites(files, data):
    """
    Return sites present in every selected file, preserving first-file order.
    """
    if not files:
        return []

    first_file = files[0]
    first_data = data[first_file]
    return [
        site for site in first_data
        if all(site in data[fname] for fname in files)
    ]


def common_codes_for_site_pair(files, data, source, target):
    """
    Return code names present for source and target in every selected file.
    """
    if not files or not source or not target or source == target:
        return []

    try:
        first_source_codes = data[files[0]][source]
        first_target_codes = data[files[0]][target]
    except KeyError:
        return []

    codes = []
    for code in first_source_codes:
        if code not in first_target_codes:
            continue
        if all(
            source in data[fname]
            and target in data[fname]
            and code in data[fname][source]
            and code in data[fname][target]
            for fname in files
        ):
            codes.append(code)

    return codes


def _get_sequence(data, filename, site, code):
    try:
        return data[filename][site][code]
    except KeyError:
        raise ValueError(
            f"Missing site/code {site}/{code} in {filename}."
        ) from None


def _validate_sequences(source_seq, target_seq):
    source_values = _sequence_values(source_seq)
    target_values = _sequence_values(target_seq)

    if len(source_values) != len(target_values):
        raise ValueError("Synchronization sequences must have the same length.")
    if len(source_values) == 0:
        raise ValueError("Synchronization cannot be computed on empty sequences.")

    source_labels = _alphabet_labels(source_seq)
    target_labels = _alphabet_labels(target_seq)
    if source_labels and target_labels and source_labels != target_labels:
        raise ValueError(
            "Synchronization sequences must have compatible alphabets."
        )


def build_synchronization_table(files, data, source, target, code):
    """
    Build the synchronization likelihood, mutual information, and direction CSV.
    """
    if not files:
        raise ValueError("Load at least one file to compute synchronization.")
    if not source:
        raise ValueError("Select a source site.")
    if not target:
        raise ValueError("Select a target site.")
    if source == target:
        raise ValueError("Select different source and target sites.")
    if not code:
        raise ValueError("Select a code.")

    headers = ["Filename", "Source", "Target", "Code", "SLH", "MI", "Dir"]
    rows = []

    for filename in files:
        source_seq = _get_sequence(data, filename, source, code)
        target_seq = _get_sequence(data, filename, target, code)
        _validate_sequences(source_seq, target_seq)

        slh = synchronization_likelihood(source_seq, target_seq)
        mi = mutual_information(source_seq, target_seq)
        direction = mcr(source_seq, target_seq) - mcr(target_seq, source_seq)

        rows.append([filename, source, target, code, slh, mi, direction])

    return headers, rows


def synchronization_filename(source, target, code):
    """
    Return the CSV filename for the selected source, target, and code.
    """
    return "_".join([
        str(source),
        str(target),
        str(code),
        OUTPUT_DIR,
    ]) + TABLE_EXT


def to_csv_lines(headers, rows):
    """
    Convert a synchronization table into semicolon-separated CSV lines.
    """
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=SEP, lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return buffer.getvalue().splitlines(keepends=True)


def default_site_pair(sites):
    """
    Return the preferred source and target pair for the current sites.
    """
    if "Aidant" in sites and "Patient" in sites:
        return "Aidant", "Patient"
    if len(sites) >= 2:
        return sites[0], sites[1]
    if sites:
        return sites[0], ""
    return "", ""


class SynchronizationTool:
    """
    Dedicated analyser tab for synchronization likelihood and direction.
    """

    def __init__(self, parent):
        self.parent = parent
        self.selected_files = []
        self.gdata = {}
        self.sites = []

        self.tab = parent.notebook.add("Synchronization")
        doc_frame = tkinter.LabelFrame(
            self.tab,
            text="Synchronization likelihood and direction",
        )
        tkinter.Label(
            doc_frame,
            text="Compute synchronization likelihood, mutual information, "
                 "and direction for a source-target pair.",
        ).grid(sticky=tkinter.W)
        doc_frame.grid(column=0, row=0, sticky=tkinter.W)

        select_frame = tkinter.LabelFrame(self.tab, text="Site and code")
        select_frame.grid(column=0, row=1, sticky=tkinter.W)

        self.source_choice = Pmw.ScrolledListBox(
            select_frame,
            items=[],
            labelpos="nw",
            label_text="Source site",
        )
        self.source_choice.configure(listbox_selectmode="browse",
                                     listbox_exportselection=False)
        self.source_choice.grid(column=0, row=0)
        self.source_choice.component("listbox").bind(
            "<<ListboxSelect>>",
            self._on_site_selection_change,
        )

        self.target_choice = Pmw.ScrolledListBox(
            select_frame,
            items=[],
            labelpos="nw",
            label_text="Target site",
        )
        self.target_choice.configure(listbox_selectmode="browse",
                                     listbox_exportselection=False)
        self.target_choice.grid(column=1, row=0)
        self.target_choice.component("listbox").bind(
            "<<ListboxSelect>>",
            self._on_site_selection_change,
        )

        self.code_choice = Pmw.ScrolledListBox(
            select_frame,
            items=[],
            labelpos="nw",
            label_text="Code",
        )
        self.code_choice.configure(listbox_selectmode="browse",
                                   listbox_exportselection=False)
        self.code_choice.grid(column=2, row=0)

        launch_but = tkinter.Button(
            self.tab,
            text="Compute synchronization likelihood and direction",
            command=self.launch,
        )
        launch_but.grid(column=0, row=2, sticky=tkinter.W)

    def _select_value(self, scrolled_listbox, items, value):
        listbox = scrolled_listbox.component("listbox")
        listbox.selection_clear(0, tkinter.END)
        if value in items:
            listbox.selection_set(items.index(value))

    def _selected_value(self, scrolled_listbox):
        selection = scrolled_listbox.getcurselection()
        return selection[0] if selection else ""

    def _on_site_selection_change(self, event=None):
        self.update_code_choices()

    def update_state(self, state):
        """
        Update selectable sites and codes after files are loaded.
        """
        self.selected_files = state["files"]
        self.gdata = state["data"]
        self.sites = common_sites(self.selected_files, self.gdata)

        self.source_choice.setlist(self.sites)
        self.target_choice.setlist(self.sites)

        source, target = default_site_pair(self.sites)
        self._select_value(self.source_choice, self.sites, source)
        self._select_value(self.target_choice, self.sites, target)
        self.update_code_choices()

    def update_code_choices(self):
        """
        Refresh the code list from the currently selected source and target.
        """
        previously_selected = self._selected_value(self.code_choice)
        source = self._selected_value(self.source_choice)
        target = self._selected_value(self.target_choice)
        codes = common_codes_for_site_pair(
            self.selected_files,
            self.gdata,
            source,
            target,
        )

        self.code_choice.setlist(codes)
        if previously_selected in codes:
            self._select_value(self.code_choice, codes, previously_selected)
        elif codes:
            self._select_value(self.code_choice, codes, codes[0])

    def launch(self):
        """
        Compute synchronization metrics and write a CSV into the output folder.
        """
        source = self._selected_value(self.source_choice)
        target = self._selected_value(self.target_choice)
        code = self._selected_value(self.code_choice)

        try:
            headers, rows = build_synchronization_table(
                self.selected_files,
                self.gdata,
                source,
                target,
                code,
            )
        except Exception as exc:
            tkinter.messagebox.showerror(
                title="Could not compute synchronization",
                message=str(exc),
            )
            return

        initialdir = os.path.join(self.parent.cwd, OUTPUT_DIR)
        try:
            pathlib.Path(initialdir).mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            tkinter.messagebox.showerror(
                title="Could not create output folder",
                message=str(exc),
            )
            return

        outdir = tkinter.filedialog.askdirectory(initialdir=initialdir,
                                                 mustexist=True)
        if not outdir:
            return

        outfile = os.path.join(outdir,
                               synchronization_filename(source, target, code))
        try:
            with open(outfile, "w", encoding="utf-8", newline="") as datafile:
                datafile.writelines(to_csv_lines(headers, rows))
        except OSError as exc:
            tkinter.messagebox.showerror(
                title="Could not write synchronization CSV",
                message=str(exc),
            )
            return

        tkinter.messagebox.showinfo(title="Synchronization CSV written",
                                    message=outfile)
