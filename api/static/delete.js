function deleteNote(noteId) {
  fetch("/delete", {
    method: "POST",
    body: JSON.stringify({ note_id: noteId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
