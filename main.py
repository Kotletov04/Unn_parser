from search.search import SearchNN

LOGIN = '*****'
PASSWORD = '*****'

if __name__ == '__main__':
    SearchNN(login=LOGIN, password=PASSWORD, mode='file').get_raz(4)
    SearchNN(login=LOGIN, password=PASSWORD, mode='file').studednts(60)



