from django import forms


class IntegrationConfigForm(forms.Form):
    youtube_channel_url = forms.URLField(label="URL канала YouTube")
    youtube_count_videos = forms.IntegerField(label="Количество видео")
    youtube_playlists = forms.MultipleChoiceField(
        label="Плейлисты", choices=[], required=False
    )
    reviews_service_name = forms.CharField(label="Название сервиса отзывов")
    reviews_count = forms.IntegerField(label="Количество отзывов")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "youtube_channel_url" in kwargs:
            self.fields["youtube_playlists"].choices = self.get_playlists(
                kwargs["youtube_channel_url"]
            )

    def get_playlists(self, channel_url):
        return ["qwerty", "abc"]
