from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticatedOrReadOnly
from .repositories.repository import BookRepository
from .serializers.serializers import BookSerialzer, BookCreateSerializer, BookUpdateSerializer
from .models import Book
from .services.book_services import BookService
from rest_framework.response import Response
from rest_framework.views import APIView




book_service=BookService()

def get_book_persmissions(request):
    if request.method in ['GET','HEAD','OPTIONS']:
        return [AllowAny()]
    else : 
        return [IsAdminUser()]

# class BookViewSet(viewsets.ModelViewSet):
#     repo = BookRepository()
#     serializer_class=BookSerialzer
#     permission_classes=[IsAuthenticatedOrReadOnly]
#     lookup_field='pk'
    
    
#     def get_queryset(self):
#         return self.repo.get_all()

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return BookCreateSerializer
#         if self.action in ['update','partial_update']:
#             return BookUpdateSerializer
#         return BookSerialzer


#     def list(self,request,*arg,**kwarg):
#         author_query = request.query_params.get('author')
#         title_query= request.query_params.get('title')
#         available_only=request.query_params.get('available','false').lower()=='true'
        
#         if title_query :
#             service_response = book_service.search_books_by_title(title_query)
#         elif author_query : 
#             service_response= book_service.filter_books_by_author(author_query)
#         elif available_only :
#             service_response=book_service.get_available_books()
#         else :
#             service_response=book_service.get_all_books()

#         if service_response["success"]:
#             serializer=self.get_serializer(service_response['data'],many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response({"detail":service_response['message']}, status=status.HTTP_400_BAD_REQUEST)
        

#     def retrieve(self, request, pk=None):
#         service_response = book_service.get_book_by_id(pk)

#         if service_response["success"]:
#             serializer=BookSerialzer(service_response["data"])
#             return Response(serializer.data,status=status.HTTP_200_OK)
        
#         return Response({"detail": service_response['message']}, status.HTTP_404_NOT_FOUND)
    
#     def create(self, request, *args, **kwargs):
#         serializer=self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         service_response=book_service.create_book(serializer.validated_data)

#         if service_response['success']:
#             response_serializer=self.get_serializer(service_response['data'])
#             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
#         return Response({'detail': service_response["message"]}, status=status.HTTP_400_BAD_REQUEST)
    
#     def update(self, request, pk=None,*args, **kwargs):
#         partial=kwargs.pop('partial',False)
#         try :
#             book_instance=Book.objects.get(pk=pk)
#         except Book.DoesNotExist : 
#             return Response({"detai:"f"Book with id : {pk} not found"},status=status.HTTP_404_NOT_FOUND)
        
#         serializer=self.get_serializer(book_instance, data=request.data,partial=partial)
#         serializer.is_valid(raise_exception=True)
        
#         service_response=book_service.update_book(pk,serializer.validated_data)

#         if service_response["success"]:
#             response_serializer=self.get_serializer(service_response["data"])
#             return Response(response_serializer.data,status=status.HTTP_200_OK)
#         return Response({"detail:":service_response["message"] },status=status.HTTP_400_BAD_REQUEST)
    
#     def destroy(self, request,pk):
#         service_response=book_service.delete_book(pk)
#         if service_response['success']:
#             return Response(status=status.HTTP_200_OK)
#         return Response({'detail':service_response['message']},status=status.HTTP_404_NOT_FOUND)
    
class BookListCreateView(APIView):
    def get_permissions(self):
        return get_book_persmissions(self.request)
    
    def get(self,request,format=None):
        author_query = request.query_params.get('author')
        title_query= request.query_params.get('title')
        available_only=request.query_params.get('available','false').lower()=='true'
        
        if title_query :
            service_response = book_service.search_books_by_title(title_query)
        elif author_query : 
            service_response= book_service.filter_books_by_author(author_query)
        elif available_only :
            service_response=book_service.get_available_books()
        else :
            service_response=book_service.get_all_books()

        if service_response["success"]:
            serializer=BookSerialzer(service_response['data'],many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"detail":service_response['message']}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,format=None):
        serializer=BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service_response=book_service.create_book(serializer.validated_data)

        if service_response['success']:
            response_serializer=BookSerialzer(service_response['data'])
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'detail': service_response["message"]}, status=status.HTTP_400_BAD_REQUEST)
    
    



class BookDetailView(APIView):
    def get_permissions(self):
        return get_book_persmissions(self.request)
    def get_book_instance(self,pk):
        service_response = book_service.get_book_by_id(pk)

        if service_response["success"]:
            return service_response['data']
        raise Response({"detail": service_response['message']}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self,request,pk,format=None):
        service_response = book_service.get_book_by_id(pk)

        if service_response["success"]:
            serializer=BookSerialzer(service_response["data"])
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response({"detail": service_response['message']}, status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk,format=None):
        book_instance= self.get_book_instance(pk)
        if isinstance(book_instance,Response):
            return book_instance
        
        serializer=BookUpdateSerializer(book_instance,data=request.data,partial=False)
        serializer.is_valid(raise_exception=True)

        service_response=book_service.update_book(pk,serializer.validated_data)

        if service_response["success"]:
            response_serializer=BookSerialzer(service_response["data"])
            return Response(response_serializer.data,status=status.HTTP_200_OK)
        return Response({"detail:":service_response["message"] },status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request,pk,format=None):
        book_instance= self.get_book_instance(pk)
        if isinstance(book_instance,Response):
            return book_instance
        
        serializer=BookUpdateSerializer(book_instance,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)

        service_response=book_service.update_book(pk,serializer.validated_data)

        if service_response["success"]:
            response_serializer=BookSerialzer(service_response["data"])
            return Response(response_serializer.data,status=status.HTTP_200_OK)
        return Response({"detail:":service_response["message"] },status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        service_response=book_service.delete_book(pk)
        if service_response['success']:
            return Response(status=status.HTTP_200_OK)
        return Response({'detail':service_response['message']},status=status.HTTP_404_NOT_FOUND)
    