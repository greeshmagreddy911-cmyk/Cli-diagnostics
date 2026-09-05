from scraper import generate_summary


def test_generate_summary():
    data = [
        {"title": "Book 1", "price": "£10.00", "rating": "Three"},
        {"title": "Book 2", "price": "£20.00", "rating": "Three"},
        {"title": "Book 3", "price": "£15.00", "rating": "Five"},
    ]

    summary = generate_summary(data)

    assert summary["total_books"] == 3
    assert summary["rating_distribution"]["Three"] == 2
    assert summary["rating_distribution"]["Five"] == 1
