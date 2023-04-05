window.onload = function () {
    document.querySelectorAll('.page-link').forEach(element => { element.addEventListener('click', movePage); });

    document.getElementById('filterForm').addEventListener('reset', function () {
        document.querySelectorAll('a.btn.active').forEach(buttonElement => {
            bootstrap.Button.getOrCreateInstance(buttonElement).toggle();
        });
    });

    document.getElementById('filterForm').addEventListener('submit', function () {
        document.querySelectorAll('a.btn.active').forEach(buttonElement => {
            buttonElement.firstElementChild.checked = "checked";
        });
    });
};

function movePage() {
    document.getElementById('page').value = this.dataset.page;
    document.getElementById('filterForm').submit();
}