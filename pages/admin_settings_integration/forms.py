from django import forms


class IntegrationConfigForm(forms.Form):
    youtube_channel_url = forms.URLField(label="URL канала YouTube")
    youtube_count_videos = forms.IntegerField(label="Количество видео")
    youtube_playlists = forms.CharField(
        label="Плейлисты", widget=forms.Textarea, help_text="разделять символами ', '"
    )
    reviews_service_name = forms.CharField(label="Название сервиса отзывов")
    reviews_count = forms.IntegerField(label="Количество отзывов")
