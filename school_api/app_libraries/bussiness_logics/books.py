from typing import List

from school_api.app_libraries.models import Book, BorrowHistory


class BookBL:
    def _get_nearest_return_date(self, book: Book):
        borrow_obj: BorrowHistory = book.borrow_histories.filter(is_borrowed=1).order_by("deadline_date").first()
        if not borrow_obj:
            return None
        return borrow_obj.deadline_date

    def sync_qty_for_borrowed_book(self, borrow_history_objects: List[BorrowHistory]):
        for borrow in borrow_history_objects:
            book = borrow.book
            book.quantity -= 1

            if book.quantity == 0:
                book.nearest_return_date = self._get_nearest_return_date(book)

            book.save()

    def sync_qty_for_returned_book(self, borrow_history_objects: List[BorrowHistory]):
        for borrow in borrow_history_objects:
            book = borrow.book
            if book.quantity == 0:
                book.nearest_return_date = None

            book.quantity += 1

            book.save()
