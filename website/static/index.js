
//takes id that we passed and sends post reqeust to delete note endpoint

//When it gets a response, it will reload the window and send us back to the homepage (refresh the page)
function deleteNote(noteId) {
    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId })
    }).then((_res) => {
        window.location.href = '/'
    })

}