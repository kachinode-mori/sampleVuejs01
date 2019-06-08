from django.db import models
from django.contrib.auth import get_user_model as user_model
from datetime import datetime


User = user_model()

class Want(models.Model):
    STATUS_NOSTART = "nostart"
    STATUS_DOING = "doing"
    STATUS_DONE = "done"
    STATUS_SET = (
            (STATUS_NOSTART, "未着手"),
            (STATUS_DOING, "実施中"),
            (STATUS_DONE, "達成"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wants')       # ユーザID
    content = models.CharField(max_length=256)                                           # want内容
    status = models.CharField(choices=STATUS_SET, default=STATUS_NOSTART, max_length=8)  # ステータス(0:未着手/1:実施中/2:達成)
    target_date = models.DateTimeField(null=True, blank=True)                            # 目標日付
    publish_set = models.BooleanField(default=True)                                      # 公開設定(0:非公開/1:公開)
    achieve_date = models.DateTimeField(null=True, blank=True)                           # 達成日付
    achieve_text = models.TextField(null=True, blank=True)                               # 達成コメント
    achieve_url = models.URLField(null=True, blank=True)                                 # 達成参照リンク
    like_num = models.IntegerField(default=0)                                            # likes数
    display_order = models.IntegerField(default=0)                                       # 表示並び順(19/01/08追加)
    create_date = models.DateTimeField(default=datetime.now())                           # 登録日付

    class Meta:
        db_table = 'wants'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')    # いいねしたユーザID
    want = models.ForeignKey(Want, on_delete=models.CASCADE, related_name='likes')    # WantID

    class Meta:
        db_table = 'likes'

    # null: データベス内にNULLとして値を保持する
    # blank: フィールドがブランクなることが許容される
