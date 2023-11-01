const board = document.getElementById('board-container');
const moves = document.getElementById('doc-moves');
const title = document.getElementById('doc-title');

window.addEventListener('resize', () => {

  const viewport_x = window.innerWidth;
  const viewport_y = window.innerHeight;
  let breakpoint_lg = window
    .getComputedStyle(document.documentElement)
    .getPropertyValue("--bs-breakpoint-lg")
  breakpoint_lg = parseInt(breakpoint_lg);

  if (viewport_x >= breakpoint_lg) {
      const board_width = board.offsetWidth;
      const title_height = title.offsetHeight;
      const board_height = Math.min(board_width, viewport_y-60);
      const moves_height = board_height - title_height;

      moves.style.height = `${moves_height}px`;
      board.style.height = `${board_height}px`;
  } else {
      moves.style.height = 'fit-content';
      board.style.height = 'auto';
  }
});

window.dispatchEvent(new Event('resize'));