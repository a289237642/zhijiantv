webpackJsonp([20],{QNIc:function(t,e){},oWp2:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i={name:"typeManagement",data:function(){var t=this;return{editModal:!1,table:{page:1,pagesize:10,total:0,editgroupId:0,columns:[{title:"序号",key:"sort",width:130,align:"center"},{title:"课程ID",key:"type_id",width:130,align:"center"},{title:"类型名称",key:"name",align:"center"},{title:"操作",align:"center",render:function(e,a){return e("div",{style:{display:"2"==a.row.is_show?"none":"inline-block"}},[e("i-switch",{attrs:{title:"0"==a.row.is_show?"未上架":"已上架"},props:{value:a.row.is_show+"",trueValue:"1",falseValue:"0"},on:{"on-change":function(e){t.changeStatus(a.row.type_id,e)}}}),e("i",{attrs:{class:"iconfont icon-edit"},on:{click:function(){t.showEditModal("edit",a.row),t.table.editgroupId=a.row.type_id}}}),e("i",{attrs:{class:"iconfont icon-delete"},style:{color:"#ffc639"},on:{click:function(){t.$Modal.warning({content:"确定删除该爆料类型吗?",onOk:function(){t.$http.post(t.PATH.DELETE_LESSON_TYPE,{type_id:a.row.type_id}).then(function(e){0===e.data.errno&&t.getSubject("z")})}})}}})])}}],data:[]},formValidate:{type:"new",row:{},content:"",sort:""},ruleValidate:{sort:[{required:!0,message:"序号",trigger:"blur"}],content:[{required:!0,message:"请输入类型名称",trigger:"blur"}]}}},methods:{changePage:function(t){this.table.page=t,this.getSubject()},getSubject:function(t){var e=this,a={};a=t?{page:1,pagesize:10}:{page:this.table.page,pagesize:this.table.pagesize},this.$post(this.PATH.GET_LESSON_TYPE,a).then(function(t){0==t.data.errno?(e.table.total=t.data.count,e.table.data=t.data.data):e.$Modal.error({width:360,content:t.data.errmsg})})},changeStatus:function(t,e){var a=this;this.$http.post(this.PATH.STATUS_LESSON_TYPE,{type_id:t}).then(function(t){0===t.data.errno?a.getSubject():(a.getSubject(),a.$Modal.error({width:360,content:t.data.msg}))})},showEditModal:function(t,e){this.formValidate.type=t,"new"==t?(this.$refs.formValidate.resetFields(),this.formValidate.type_id="",this.formValidate.content="",this.formValidate.sort=""):(this.formValidate.type_id=e.type_id,this.formValidate.content=e.name,this.formValidate.sort=e.sort.toString()),this.editModal=!0},submitForm:function(t){var e=this,a=this.formValidate.content;this.$refs[t].validate(function(t){if(t){var i=e.formValidate.type,o=void 0,n=new Object;"new"==i?(o=e.PATH.ADD_LESSON_TYPE,n={name:a,sort:e.formValidate.sort}):(o=e.PATH.EDIT_LESSON_TYPE,n={name:a,type_id:e.table.editgroupId,sort:e.formValidate.sort}),e.$post(o,n).then(function(t){e.formValidate.type,e.$Modal.success({title:"提示",content:t.data.errmsg,onOk:function(){e.editModal=!1}}),e.getSubject()})}else e.$Message.error("Fail!")})}},created:function(){this.getSubject()}},o={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"typeManagement"}},[a("div",{staticClass:"h1"},[t._v("课程类型管理")]),t._v(" "),a("div",{staticClass:"header"},[a("Button",{staticClass:"newbtn zhijian-new-btn",attrs:{type:"primary"},on:{click:function(e){t.showEditModal("new")}}},[t._v("新增")])],1),t._v(" "),a("Table",{staticClass:"zhijian-table account-table",attrs:{stripe:"",columns:t.table.columns,data:t.table.data}}),t._v(" "),a("div",{staticClass:"zhijian-pagination"},[a("Page",{attrs:{total:t.table.total,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePage}})],1),t._v(" "),a("Modal",{attrs:{"mask-closable":!1,width:"535","class-name":"ma-edit-modal"},model:{value:t.editModal,callback:function(e){t.editModal=e},expression:"editModal"}},[a("div",{staticClass:"edit-modal-body"},[a("Icon",{attrs:{type:"android-close"},on:{click:function(e){t.editModal=!1}}}),t._v(" "),"new"==t.formValidate.type?a("div",{staticClass:"title"},[t._v("新增类型")]):t._e(),t._v(" "),"edit"==t.formValidate.type?a("div",{staticClass:"title"},[t._v("编辑类型")]):t._e(),t._v(" "),a("Form",{ref:"formValidate",attrs:{model:t.formValidate,rules:t.ruleValidate,"label-width":100}},[a("FormItem",{attrs:{label:"排序",prop:"sort"}},[a("Input",{attrs:{type:"text",placeholder:"Enter something..."},model:{value:t.formValidate.sort,callback:function(e){t.$set(t.formValidate,"sort",e)},expression:"formValidate.sort"}})],1),t._v(" "),a("FormItem",{attrs:{label:"类型名称",prop:"content"}},[a("Input",{attrs:{type:"text",placeholder:"Enter something..."},model:{value:t.formValidate.content,callback:function(e){t.$set(t.formValidate,"content",e)},expression:"formValidate.content"}})],1)],1)],1),t._v(" "),a("div",{staticClass:"zhijian-btn-box"},[a("div",{staticClass:"zhijian-btn-confirm",on:{click:function(e){t.submitForm("formValidate")}}},[t._v("确定")])])])],1)},staticRenderFns:[]};var n=a("VU/8")(i,o,!1,function(t){a("QNIc")},null,null);e.default=n.exports}});