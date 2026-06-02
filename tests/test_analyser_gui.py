from pathlib import Path

from scyseqtools.analyser import analyser


class FakeVar:
    def __init__(self, value=''):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class FakeAvailable:
    def __init__(self, selection=()):
        self.items = []
        self.selection = tuple(selection)

    def setlist(self, items):
        self.items = list(items)

    def getcurselection(self):
        return self.selection


class FakeSelected:
    def __init__(self, value=''):
        self.value = value

    def setvalue(self, value):
        self.value = value


class FakeMethod:
    def __init__(self):
        self.states = []

    def update_state(self, state):
        self.states.append(state)


def make_fake_app(data_dir, selection=()):
    app = object.__new__(analyser.Application)
    app.data = {}
    app.ddir = FakeVar(str(data_dir))
    app.cwd = None
    app.available = FakeAvailable(selection)
    app.selected = FakeSelected()
    app.methods = [FakeMethod()]
    return app


def test_analyzer_dir_for_uses_data_directory_sibling(tmp_path):
    data_dir = tmp_path / 'project' / 'data'

    assert analyser._analyzer_dir_for(str(data_dir)) == str(
        tmp_path / 'project' / 'analyzer_files'
    )


def test_get_directory_lists_files_without_creating_analyzer_folder(tmp_path, monkeypatch):
    project_dir = tmp_path / 'project'
    data_dir = project_dir / 'data'
    data_dir.mkdir(parents=True)
    (data_dir / 'first.cdx').write_text('{}', encoding='utf-8')
    app = make_fake_app('')

    monkeypatch.setattr(
        analyser.tkinter.filedialog,
        'askdirectory',
        lambda initialdir: str(data_dir),
    )

    analyser.Application.get_directory(app)

    assert app.ddir.get() == str(data_dir)
    assert app.available.items == ['first.cdx']
    assert app.selected.value == ''
    assert not (project_dir / 'analyzer_files').exists()


def test_load_file_creates_analyzer_folder_after_success(tmp_path, monkeypatch):
    project_dir = tmp_path / 'project'
    data_dir = project_dir / 'data'
    data_dir.mkdir(parents=True)
    app = make_fake_app(data_dir, selection=('first.cdx',))
    loaded = {'site': {'code': object()}}

    monkeypatch.setattr(analyser.IO, 'read_codix', lambda fname: loaded)

    analyser.Application.load_file(app)

    assert (project_dir / 'analyzer_files').is_dir()
    assert app.cwd == str(project_dir / 'analyzer_files')
    assert app.data == {'first.cdx': loaded}
    assert app.selected.value == 'first.cdx'
    assert app.methods[0].states[-1]['files'] == ['first.cdx']


def test_load_file_replaces_previous_selection(tmp_path, monkeypatch):
    project_dir = tmp_path / 'project'
    data_dir = project_dir / 'data'
    data_dir.mkdir(parents=True)
    app = make_fake_app(data_dir, selection=('first.cdx',))
    loaded_by_name = {
        'first.cdx': {'site': {'code': object()}},
        'second.cdx': {'site': {'code': object()}},
    }

    def read_codix(fname):
        return loaded_by_name[Path(fname).name]

    monkeypatch.setattr(analyser.IO, 'read_codix', read_codix)

    analyser.Application.load_file(app)
    app.available.selection = ('second.cdx',)
    analyser.Application.load_file(app)

    assert app.data == {'second.cdx': loaded_by_name['second.cdx']}
    assert app.selected.value == 'second.cdx'
    assert app.methods[0].states[-1]['files'] == ['second.cdx']
    assert app.methods[0].states[-1]['data'] == app.data


def test_invalid_load_does_not_create_folder_or_replace_previous_state(
        tmp_path, monkeypatch):
    project_dir = tmp_path / 'project'
    data_dir = project_dir / 'data'
    data_dir.mkdir(parents=True)
    app = make_fake_app(data_dir, selection=('bad.cdx',))
    old_data = {'old.cdx': {'site': {'code': object()}}}
    app.data = old_data
    app.cwd = str(tmp_path / 'old_analyzer_files')
    app.selected.value = 'old.cdx'
    errors = []

    monkeypatch.setattr(
        analyser.IO,
        'read_codix',
        lambda fname: (_ for _ in ()).throw(ValueError('bad data')),
    )
    monkeypatch.setattr(
        analyser.tkinter.messagebox,
        'showerror',
        lambda title, message: errors.append((title, message)),
    )

    analyser.Application.load_file(app)

    assert errors == [('Could not load data file', 'bad data')]
    assert not (project_dir / 'analyzer_files').exists()
    assert app.data is old_data
    assert app.cwd == str(tmp_path / 'old_analyzer_files')
    assert app.selected.value == 'old.cdx'
    assert app.methods[0].states == []


def test_working_directory_creation_failure_preserves_previous_state(
        tmp_path, monkeypatch):
    project_dir = tmp_path / 'project'
    data_dir = project_dir / 'data'
    data_dir.mkdir(parents=True)
    (project_dir / 'analyzer_files').write_text('not a directory',
                                                encoding='utf-8')
    app = make_fake_app(data_dir, selection=('first.cdx',))
    old_data = {'old.cdx': {'site': {'code': object()}}}
    app.data = old_data
    app.cwd = str(tmp_path / 'old_analyzer_files')
    app.selected.value = 'old.cdx'
    errors = []

    monkeypatch.setattr(
        analyser.IO,
        'read_codix',
        lambda fname: {'site': {'code': object()}},
    )
    monkeypatch.setattr(
        analyser.tkinter.messagebox,
        'showerror',
        lambda title, message: errors.append((title, message)),
    )

    analyser.Application.load_file(app)

    assert errors[0][0] == 'Could not create working directory'
    assert app.data is old_data
    assert app.cwd == str(tmp_path / 'old_analyzer_files')
    assert app.selected.value == 'old.cdx'
    assert app.methods[0].states == []
