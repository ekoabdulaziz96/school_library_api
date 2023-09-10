# static
BORROW_MIN_BOOK = 1
BORROW_MAX_BOOK = 10
BORROW_DEADLINE_DAYS = 30
BORROW_EXTEND_MAX_COUNT = 1

# message
MSG_STUDENT_NOT_FOUND = "Student not found."
MSG_BORROW_SUCCESS = "Success add {} borrowed book to {}."
MSG_BORROW_RETURN_SUCCESS = "Success return {} borrowed book from {}."
MSG_BORROW_EXTEND_SUCCESS = "Success extend {} borrowed book from {}."
MSG_BORROW_INVALID_MIN_COUNT = "Choose at least {} book.".format(BORROW_MIN_BOOK)
MSG_BORROW_INVALID_MAX_COUNT = "Exceed the quota, maximum {} books.".format(BORROW_MAX_BOOK)
MSG_BORROW_INVALID_BOOK_UUID = "There are some books that cannot be found."
MSG_BORROW_INVALID_BOOK_QTY = "Choosen book out of stok. book title: {}"
MSG_BORROW_BORROWED_YET = "Choosen book have been borrowed. book title: {}"
MSG_BORROW_RETURNED_YET = "Choosen book have been returned. book title: {}"
MSG_BORROW_INVALID_EXTEND = "Choosen book can't be extended. book title: {}"
