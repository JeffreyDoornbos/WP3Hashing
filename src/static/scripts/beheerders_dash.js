//clear data on reload to allow for table refresh and remove unnecessary cached data
window.localStorage.removeItem('Onderzoeken_3');
window.localStorage.removeItem('Onderzoeken_2');
window.localStorage.removeItem('Ervaringsdeskundigen_3');
window.localStorage.removeItem('Ervaringsdeskundigen_2');
window.localStorage.removeItem('Deelnamen_3');
window.localStorage.removeItem('Deelnamen_2');

let table_afwachting_onderzoek = document.querySelector("tbody[data-target-status='3'][data-target-table='onderzoeken']"),
table_afgekeurd_onderzoek = document.querySelector("tbody[data-target-status='2'][data-target-table='onderzoeken']"),
table_afwachting_ervaringsdeskundigen = document.querySelector("tbody[data-target-status='3'][data-target-table='ervaringsdeskundigen']"),
table_afgekeurd_ervaringsdeskundigen = document.querySelector("tbody[data-target-status='2'][data-target-table='ervaringsdeskundigen']"),
table_afwachting_deelnamen = document.querySelector("tbody[data-target-status='3'][data-target-table='deelnamen']"),
table_afgekeurd_deelnamen = document.querySelector("tbody[data-target-status='2'][data-target-table='deelnamen']");

document.querySelectorAll("btn[type='submit']").forEach((el) => {
    el.addEventListener('click', (ev) => {
        var target = ev.target;
        if (target == null || target.getAttribute('data-target-table') == null)
            return;
        switch (target.getAttribute('data-target-table'))
        {
            case "onderzoeken":
                window.localStorage.removeItem("Onderzoeken_3");
                window.localStorage.removeItem("Onderzoeken_2");
                break;
            case "ervaringsdeskundigen":
                window.localStorage.removeItem("Ervaringsdeskundigen_3");
                window.localStorage.removeItem("Ervaringsdeskundigen_2");
                break;
            case "deelnamen":
                window.localStorage.removeItem("Deelnamen_3");
                window.localStorage.removeItem("Deelnamen_2");
                break;
        }
        query_ajax();
    });
});

//Every 3 seconds, query the polling endpoint for changes
//The interval id is saved so if needed you can use clearInterval(interval) to stop polling
let interval = setInterval(query_ajax, 3000);
query_ajax(); //Initial request to set data and render tables

function query_ajax() 
{
    if (table_afwachting_onderzoek != null)
    {
        $.get(
        {
            url: '/poll/?table=onderzoeken&status=3',
            dataType: 'json'
        }).done((data, status) => validateValue(data, status, 'Onderzoeken_3', '/render_table/onderzoeken/3/', table_afwachting_onderzoek));
    }
    if (table_afgekeurd_onderzoek != null)
    {
        $.get(
        {
            url: '/poll/?table=onderzoeken&status=2',
            dataType: 'json'
        }).done((data, status) => validateValue(data, status, 'Onderzoeken_2', '/render_table/onderzoeken/2/', table_afgekeurd_onderzoek));
    }
    if (table_afwachting_ervaringsdeskundigen != null)
    {
        $.get(
        {
            url: '/poll/?table=ervaringsdeskundigen&status=3',
            dataType: 'json'
        }).done((data, status) => validateValue(data, status, "Ervaringsdeskundigen_3", '/render_table/ervaringsdeskundigen/3/', table_afwachting_ervaringsdeskundigen));
    }
    if (table_afgekeurd_ervaringsdeskundigen != null)
    {
        $.get(
        {
            url: '/poll/?table=ervaringsdeskundigen&status=2',
            dataType: 'json'
        }).done((data, status) => validateValue(data, status, "Ervaringsdeskundigen_2", '/render_table/ervaringsdeskundigen/2/', table_afgekeurd_ervaringsdeskundigen));
    }
    if (table_afwachting_deelnamen != null)
    {
        $.get(
        {
            url: '/poll/?table=deelnamen&status=3',
            dataType: 'json'
        }).done((data, status) => validateValue(data, status, "Deelnamen_3", '/render_table/deelnamen/3/', table_afwachting_deelnamen));
    }
    if (table_afgekeurd_deelnamen != null)
    {
        $.get(
        {
            url: '/poll/?table=deelnamen&status=2',
            dataType: 'json'
        }).done((data, status) => validateValue(data, status, "Deelnamen_2", '/render_table/deelnamen/2/', table_afgekeurd_deelnamen));
    }
}

function validateValue(data, status, target, successUrl, table)
{
    if (status === 'success')
    {
        var oldValue = window.localStorage.getItem(target);
        var newValue = `${data.data}`;

        if (newValue != oldValue)
        {
            $.get(
            {
                url: successUrl,
                dataType: 'html'
            }).done(
                function (data, status)
                {
                    if (status === 'success')
                        table.innerHTML = data;
                }
            );

            window.localStorage.setItem(target, newValue);
        }
    }
}