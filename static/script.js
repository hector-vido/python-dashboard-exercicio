window.addEventListener('load', function() {
  var rows = document.querySelectorAll('.data-row');
  for (var i = 0; i < rows.length; i++) {
    rows[i].addEventListener('click', function() {
      var display = this.nextElementSibling.style.display;
      this.nextElementSibling.style.display = display == 'table-row' ? 'none' : 'table-row';
    });
  }

  var buttons = document.querySelectorAll('.actions a')
  console.log(buttons);
  for (var i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener('click', function(e) {
      e.stopPropagation();
    });
  }
});
