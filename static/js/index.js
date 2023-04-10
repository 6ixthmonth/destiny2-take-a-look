window.onload = function () {
    document.querySelectorAll('.page-link').forEach(element => { element.addEventListener('click', movePage); });

    document.querySelectorAll('input[type=checkbox]:checked').forEach(element => {
        bootstrap.Button.getOrCreateInstance(element.parentElement).toggle();
    });

    document.getElementById('filterForm').addEventListener('reset', function () {
        document.querySelectorAll('a.btn.active').forEach(buttonElement => {
            bootstrap.Button.getOrCreateInstance(buttonElement).toggle();
        });
    });

    document.getElementById('submitBtn').addEventListener('click', function () {
        document.querySelectorAll('a.btn.active').forEach(buttonElement => {
            Array.from(buttonElement.children).forEach(child => { child.checked = "checked"; });
        });
        document.getElementById('filterForm').submit();
    });
};

function movePage() {
    document.getElementById('page').value = this.dataset.page;
    document.getElementById('filterForm').submit();
}