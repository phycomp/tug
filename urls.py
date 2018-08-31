from django.urls import include, path, re_path
from .views import TugMediaDelete, Address2LatLng, TugDelete, TugPagination, TugJoin, TugEdit, TugAdd, TugDetail, Tugs	#, TugCommentSelfEdit, TugCommentEdit, TugCommentSelfDelete, TugCommentDelete, TugCommentSelf, TugSearch, TugContextEdit, TugComment, GenericPostAdd


urlpatterns=[
    path(r'', Tugs.as_view(), name='tugs'),
    path(r'add/', TugAdd.as_view(), name='tug-add'),
    path(r'join/', TugJoin.as_view(), name='tug-join'),
    path(r'edit/', TugEdit.as_view(), name='tug-edit'),
    path(r'detail/<int:tid>/', TugDetail.as_view(), name='tug-detail'),
    path(r'tug-pagination/', TugPagination.as_view(), name='tug-pagination'),
    path(r'delete/', TugDelete.as_view(), name='tug-delete'),
    path(r'addr2lat-lng/', Address2LatLng.as_view(), name='addr2lat-lng'),
    path(r'media-delete/', TugMediaDelete.as_view(), name='tug-media-delete'),
    #path(r'context-edit/', TugContextEdit.as_view(), name='tug-context-edit'),
    #path(r'search/', TugSearch.as_view(), name='tug-search'),
    #path(r'comment/', TugComment.as_view(), name='tug-comment'),
    #path(r'comment-edit/', TugCommentEdit.as_view(), name='tug-comment-edit'),
    #path(r'comment-delete/', TugCommentDelete.as_view(), name='tug-comment-delete'),
    #path(r'comment-self/', TugCommentSelf.as_view(), name='tug-comment-self'),
    #path(r'comment-self-edit/', TugCommentSelfEdit.as_view(), name='tug-comment-self-edit'),
    #path(r'comment-self-delete/', TugCommentSelfDelete.as_view(), name='tug-comment-self-delete'),
    #re_path(r'(?P<tid>\d+)/', TugEdit.as_view(), name='tug-edit'),
    #re_path(r'delete/(?P<tid>\d+)/', TugDelete.as_view(), name='tug-delete'),
    #path(r'generic-post-add/', GenericPostAdd.as_view(), name='generic-post-add'),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
