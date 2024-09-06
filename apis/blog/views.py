from rest_framework import generics, permissions
from rest_framework.response import Response
from .permissions import IsAuthorOrReadOnly

from apis.blog.models import Post
from apis.blog.serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    """
    View to list all posts or create a new post.

    - GET: Returns a list of all posts (read-only).
    - POST: Authenticated users can create a new post. The author of the post is automatically set to the current user.

    Permissions:
    - IsAuthenticatedOrReadOnly: Authenticated users can create posts, while unauthenticated users can only view them.
    - IsAuthorOrReadOnly: Ensures only the author can modify their own posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """
        Override the perform_create method to set the post's author to the current authenticated user.
        """
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific post.

    - GET: Retrieve the details of a specific post by its ID.
    - PUT/PATCH: Update the post details (only the author can do this).
    - DELETE: Delete the post (only the author can do this).

    Permissions:
    - IsAuthenticatedOrReadOnly: Authenticated users can modify posts, while unauthenticated users can only view them.
    - IsAuthorOrReadOnly: Ensures only the author can update or delete their own posts.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
