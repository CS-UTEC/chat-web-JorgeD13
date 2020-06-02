$(function(){
    var url = "/messages";
    var users_link = "/users";
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
            showPageSizeSelector: true,
            allowedPageSizes: [8, 12, 20]
        },

        columns: [{
            dataField: "id",
            dataType: "number",
            allowEditing: false
        }, {
            dataField: "content",
            allowEditing: true
        }, {
            dataField: "sent_on",
            dataType: "date",
            format: "MM/dd/yyyy hh:mm"
        }, {
            dataField: "user_from_id",
            allowEditing: true,
            lookup: {
                dataSource: DevExpress.data.AspNet.createStore({
                    key: "id",
                    loadUrl : users_link,
                    insertUrl : users_link,
                    updateUrl : users_link,
                    deleteUrl : users_link,
                    onBeforeSend:function(method, ajaxOptions){
                        ajaxOptions.xhrFields = {withCredentials: true};
                    }
                }),
                valueExpr: "id",
                displayExpr: "username"
            }
        }, {
            dataField: "user_to_id",
            allowEditing: true,
            lookup: {
                dataSource: DevExpress.data.AspNet.createStore({
                    key: "id",
                    loadUrl: users_link,
                    insertUrl: users_link,
                    updateUrl: users_link,
                    deleteUrl: users_link,
                    onBeforeSend: function(method, ajaxOptions) {
                        ajaxOptions.xhrFields = {withCredentials: true};
                    }
                }),
                valueExpr: "id",
                displayExpr: "username"
            }
        } ],
    }).dxDataGrid("instance");
});