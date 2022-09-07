import json
from django.http import HttpResponse,  JsonResponse
from django.shortcuts import redirect, get_object_or_404

from django.views import View

from .forms import CommentForm
from blog.models import Article
from blog.models import Comment, BookmarkArticles
from django.templatetags.static import static

class BookmarkView(View):
    model = None

    def post(self, request, pk):
        user = request.user
        bookmark, created = self.model.objects.get_or_create(user=user, obj_id=pk)
        if not created:
            bookmark.delete()

        return HttpResponse(
            json.dumps({
                "result": created,
                "countes": self.model.objects.filter(obj_id=pk).count()

            }),
            content_type="application/json"
        )


def add_comment(request, article_id):
    form = CommentForm(request.POST or None, request.FILES or None)
    article = get_object_or_404(Article, id=article_id)

    if form.is_valid():
        comment = Comment()
        if form.cleaned_data['parent_comment']:
            comment.parent = Comment.objects.get(id=form.cleaned_data['parent_comment'])
        comment.article = article
        comment.user = request.user
        comment.content = form.cleaned_data['comment_area']
        comment.file = form.cleaned_data['file']
        comment.save()
    return redirect(article.get_absolute_url() + '#comment-' + str(comment.id))


def BlogLike(request, pk):
    post = get_object_or_404(Article, id=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        status = False
    else:
        post.likes.add(request.user)
        status = True
    result = {'count': post.likes.count(),'status': status }
    return JsonResponse(result, safe=False)


def CommentLike(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        status = False
    else:
        comment.likes.add(request.user)
        status = True
    result = {'count': comment.likes.count(), 'status' : status}
    return JsonResponse(result, safe=False)

def Bookmark(request, pk):
    bookmark, created = BookmarkArticles.objects.get_or_create(user=request.user, obj_id=pk)

    if not created:
        bookmark.delete()
        status= False
    else:
        status=True
    result = {'count': BookmarkArticles.objects.filter(obj_id=pk).count(), 'status': status}
    return JsonResponse(result, safe=False)


def ApiSearch(request):
    search = request.GET.get('search')
    query_search = list()
    if search:
        array = Article.objects.search(query=search).only('title', 'image')
        for item in array:
            result = {'image': image(item.image), 'title': item.title, 'slug':item.get_absolute_url() }
            query_search.append(result)

    # if search:
    #     query_search.append(Article.objects.search(query=search))
    #     # query_search.append(Comment.objects.search(query=search))
    #     final_set = list(chain(*query_search))
    #     final_set.sort(key=lambda x: x.create_at, reverse=True)
    #     comment = []
    #     for item in final_set:
    #         if item.__class__.__name__ == 'Comment':
    #             result = {'id': item.id,'user': item.user.username, 'article': item.article.title, 'slug': item.article.get_absolute_url(),'text': item.content}
    #             comment.append(result)
    #         if item.__class__.__name__ == 'Article':
    #             result = {'id': item.id,'user': item.user.username, 'article': item.title, 'slug': item.get_absolute_url(),'text': item.content}
    #             comment.append(result)
    #     result = serializers.serialize('json', final_set)

    return JsonResponse(query_search, safe=False)


def image(image):
    if not image:
        return static('images/small/small-3.jpg')
    return image.url