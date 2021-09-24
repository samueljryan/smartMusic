function deletePlaylist(playlistId) {
    fetch('/delete-playlist', {
      method: 'POST',
      body: JSON.stringify({ playlistId: playlistId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }