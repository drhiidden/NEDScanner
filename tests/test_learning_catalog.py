from app.core.learning_catalog import list_lessons, load_lesson_text, repo_root


def test_list_lessons_non_empty():
    lessons = list_lessons()
    assert len(lessons) >= 4


def test_load_lesson_returns_markdown():
    lessons = list_lessons()
    text = load_lesson_text(lessons[0].rel_path)
    assert len(text) > 100
    assert "#" in text


def test_learn_dir_under_repo_root():
    assert (repo_root() / "docs" / "learn" / "README.md").is_file()