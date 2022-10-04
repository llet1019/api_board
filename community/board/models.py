from django.db import models

from user.models import User


class Category(models.Model):
    category_name = models.CharField(null=False, blank=False, max_length=32, verbose_name='카테고리 명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일', )

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'
        ordering = ['created_at']


class Board(models.Model):
    category = models.ForeignKey(
        Category, null=False, blank=False, related_name='board_category', verbose_name='카테고리', on_delete=models.SET_NULL)
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='board_user', verbose_name='작성자', on_delete=models.SET_NULL
    )
    context = models.TextField(null=False, blank=False, verbose_name='본문 내용')
    view_cnt = models.PositiveIntegerField(null=False, blank=False, default=0, verbose_name='조회수')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일', )

    class Meta:
        verbose_name = '게시물'
        verbose_name_plural = '게시물'
        ordering = ['-created_at']


class BoardLike(models.Model):
    board = models.ForeignKey(
        Board, null=False, blank=False, related_name='board_like_board', verbose_name='게시물', on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='board_like_user', verbose_name='작성자', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일', )

    class Meta:
        verbose_name = '게시물 좋아요'
        verbose_name_plural = '게시물 좋아요'
        ordering = ['-created_at']


class Comment(models.Model):
    board = models.ForeignKey(
        Board, null=False, blank=False, related_name='comment_board', verbose_name='게시물', on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='comment_user', verbose_name='작성자', on_delete=models.CASCADE
    )
    context = models.TextField(null=False, blank=False, verbose_name='본문 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일', )

    class Meta:
        verbose_name = '게시물 댓글'
        verbose_name_plural = '게시물 댓글'
        ordering = ['-created_at']


class CommentLike(models.Model):
    comment = models.ForeignKey(
        Comment, null=False, blank=False, related_name='comment_like_user', verbose_name='댓글', on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, null=False, blank=False, related_name='comment_user', verbose_name='작성자', on_delete=models.CASCADE
    )
    context = models.TextField(null=False, blank=False, verbose_name='본문 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일', )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일', )

    class Meta:
        verbose_name = '게시물 좋아요'
        verbose_name_plural = '게시물 좋아요'
        ordering = ['-created_at']