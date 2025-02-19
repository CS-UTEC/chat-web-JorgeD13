$(function(){
    var url = '/users'
    $("#grid").dxDataGrid({
        dataSource: DevExpress.data.AspNet.createStore({
            key: "id",
            loadUrl: url,
            insertUrl: url,
            updateUrl: url,
            deleteUrl: url,
            onBeforeSend: function(method, ajaxOptions) {
                ajaxOptions.xhrFields = { withCredentials: true };
            }
        }),

        editing: {
            editMode: "batch",
            allowUpdating: true,
            allowDeleting: true,
            allowAdding: true
        },

        paging: {
            pageSize: 12
        },

        sorting: {
            mode: "multiple"
        },
        allowColumnReordering: "true",
        allowColumnResizing: "true",
        filterRow: {
            visible: true
        },
        pager: {
            showPageSizeSelector: false,
            allowedPageSizes: [8, 12, 20]
        },

        columns: [{
            dataField: "id",
            dataType: "number",
            allowEditing: true
        }, {
            dataField: "username"
        }, {
            dataField: "name"
        }, {
            dataField: "fullname"
        }, {
            dataField: "password"
        }, ],
    }).dxDataGrid("instance");
});