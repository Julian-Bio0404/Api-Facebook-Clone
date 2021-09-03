"""Saved views."""

# Django REST framework
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Models
from posts.models import CategorySaved, Post, Saved

# Serializers
from posts.serializers import (CategorySavedModelSerializer,
                               SavedPostModelSerializer)
    
    
@api_view(['POST'])
def create_category(request):
    """Create Saved category."""
    categories = CategorySaved.objects.filter(
        user=request.user, name=request.data['name'])

    if categories:
        data = {'message': 'you already have a collection with this name.'}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    serializer = CategorySavedModelSerializer(
            data=request.data, context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def retrieve_category(request, pk=None):
    """detail, update or delete a saved category."""
    try:
        category = CategorySaved.objects.get(user=request.user, pk=pk)
    except CategorySaved.DoesNotExist:
        data = {'message': "The collection doesn't exist."}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CategorySavedModelSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CategorySavedModelSerializer(
            category, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        posts_saved = Saved.objects.filter(user=request.user, saved_category=category)
        posts_saved.delete()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

@api_view(['POST'])
def create_saved(request, pk=None):
    """Handle post saved creation."""
    # Valida que el post y categoria existan
    try:
        post = Post.objects.get(pk=pk)
        saved_category = CategorySaved.objects.get(
            user=request.user, name=request.data['name'])
    except Post.DoesNotExist or CategorySaved.DoesNotExist:
        data = {'message': 'The category or the post does not exist.'}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    # Valida que aun no exista el post guardado
    try:
        Saved.objects.get(user=request.user, post=post)
        data = {'message': 'The saved already exists.'}
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    except Saved.DoesNotExist:
        serializer = SavedPostModelSerializer(
            data=request.data, 
            context={
                'user': request.user, 'post': post, 'saved_category': saved_category})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
def retrieve_saved(request, pk=None):
    """detail, update or delete a saved category."""
    try:
        saved = Saved.objects.get(user=request.user, pk=pk)
    except Saved.DoesNotExist:
        data = {'message': "The saved doesn't exist."}
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SavedPostModelSerializer(saved)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        saved.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_saved(request):
    """List all post saved of user."""
    saved = Saved.objects.filter(user=request.user)
    serializer = SavedPostModelSerializer(saved, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)