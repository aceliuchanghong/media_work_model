# from langchain_community.document_loaders import UnstructuredHTMLLoader
#
# # loader = UnstructuredHTMLLoader('user_crawler/liu/3356191268/liu_output.html')
# # data = loader.load()
# # print(data)
#
#
# from langchain_community.document_loaders import BSHTMLLoader
#
#
#
# loader2 = BSHTMLLoader("user_crawler/liu/3356191268/liu_output.html")
# data2 = loader2.load()
# print(data2)
# loader3 = BSHTMLLoader("user_crawler/liu/7m3lVegUOigG1Uy904GmaA/liu_output.html")
# data3 = loader3.load()
# print(data3)

from langchain_community.document_loaders import WebBaseLoader

# loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
loader = WebBaseLoader("https://www.sohu.com/a/744144846_121687421")

docs = loader.load()
print(docs)
