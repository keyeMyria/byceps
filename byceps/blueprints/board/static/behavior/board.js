onDomReady(function() {

  confirmed_post_on_click('[data-action="topic-hide"]', 'Thema verstecken?');
  confirmed_delete_on_click('[data-action="topic-unhide"]', 'Thema wieder anzeigen?');
  confirmed_post_on_click('[data-action="topic-lock"]', 'Thema schließen?');
  confirmed_delete_on_click('[data-action="topic-unlock"]', 'Thema wieder öffnen?');
  confirmed_post_on_click('[data-action="topic-pin"]', 'Thema anpinnen?');
  confirmed_delete_on_click('[data-action="topic-unpin"]', 'Thema wieder lösen?');

  confirmed_post_on_click('[data-action="posting-hide"]', 'Beitrag verstecken?');
  confirmed_delete_on_click('[data-action="posting-unhide"]', 'Beitrag wieder anzeigen?');

  var collpasedTextareas = document.querySelectorAll('textarea.collapsed');
  forEach(collpasedTextareas, function(textarea) {
    // Expand collapsible text area after receiving focus.
    textarea.addEventListener('focus', function() {
      textarea.classList.remove('collapsed');
    });

    // Collapse text area on click on cancel button.
    textarea.form.querySelector('button.cancel').addEventListener('click', function() {
      textarea.classList.add('collapsed');
    });
  });

});
