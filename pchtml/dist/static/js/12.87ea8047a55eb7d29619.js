webpackJsonp([12],{StOw:function(t,e){},jzHA:function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i={name:"keywordsManagement",data:function(){var t=this;return{editModal:!1,arcCateList:[],table:{page:1,pagesize:10,total:50,editgroupId:0,columns:[{title:"序号",key:"location",width:130,align:"center"},{title:"爆料类型名称",key:"article_group_name",align:"center"},{title:"一级关键词",key:"first_keywords",align:"center"},{title:"二级属性词",key:"second_keywords",align:"center"},{title:"操作",align:"center",render:function(e,a){return e("div",[e("i",{attrs:{class:"iconfont icon-edit"},on:{click:function(){t.showEditModal("edit",a.row)}}}),e("i",{attrs:{class:"iconfont icon-delete"},style:{color:"#ffc639"},on:{click:function(){t.$Modal.confirm({content:"确定删除吗?",onOk:function(){t.$http.post(t.PATH.DELKEYWORD,{keywords_id_list:[a.row.keyword_id]}).then(function(e){0===e.data.errno&&t.getKeywordList(1,10)})}})}}})])}}],data:[]},formValidate:{type:"new",row:{},first_keywords:"",second_keywords:"",arcCate:""},ruleValidate:{arcCate:[{required:!0,message:"请选择爆料类型",trigger:"blur",type:"number"}],first_keywords:[{required:!0,message:"请输入一级关键词",trigger:"blur"}],second_keywords:[{required:!0,message:"请输入二级属性词",trigger:"blur"}]}}},methods:{getgroups:function(){var t=this;this.$http.get(this.PATH.GROUPS).then(function(e){0==e.data.errno?t.arcCateList=e.data.data:t.$Modal.error({width:360,content:e.data.errmsg})})},getKeywordList:function(t,e){var a=this;this.$http.post(this.PATH.KEYWORDLIST,{page:t,pagesize:e}).then(function(t){0==t.data.errno?(a.table.data=t.data.data,a.table.total=t.data.count):a.$Modal.error({width:360,content:t.data.errmsg})})},changePage:function(t){this.table.page=t,this.getKeywordList(t,this.table.pagesize)},showEditModal:function(t,e){this.formValidate.type=t,"new"==t?(this.getgroups(),this.$refs.formValidate.resetFields(),this.formValidate.arcCate="",this.formValidate.group_id="",this.formValidate.content="",this.formValidate.sort=""):(this.arcCateList=[],this.formValidate.group_id=e.article_group_id,this.formValidate.keyword_id=e.keyword_id,this.formValidate.first_keywords=e.first_keywords,this.formValidate.second_keywords=e.second_keywords),this.editModal=!0},submitForm:function(t){var e=this;this.$refs[t].validate(function(t){if(t){var a=e.formValidate.type,i=void 0,r=new Object;"new"==a?(i=e.PATH.KEYWORDADD,r={article_group_id:e.formValidate.arcCate,first_keywords:e.formValidate.first_keywords,second_keywords:e.formValidate.second_keywords}):(i=e.PATH.KEYWORDUPLOAD,r={article_group_id:e.formValidate.group_id,keyword_id:e.formValidate.keyword_id,first_keywords:e.formValidate.first_keywords,second_keywords:e.formValidate.second_keywords}),e.$http.post(i,r).then(function(t){0===t.data.errno&&(e.editModal=!1,e.getKeywordList(1,10))})}else e.$Message.error("Fail!")})}},created:function(){this.getKeywordList(1,10)}},r={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"keywordsManagement"}},[a("div",{staticClass:"h1"},[t._v("文章标签管理\n    ")]),t._v(" "),a("div",{staticClass:"header"},[a("Button",{staticClass:"newbtn zhijian-new-btn",attrs:{type:"primary"},on:{click:function(e){t.showEditModal("new")}}},[t._v("新增")])],1),t._v(" "),a("Table",{staticClass:"zhijian-table account-table",attrs:{stripe:"",columns:t.table.columns,data:t.table.data}}),t._v(" "),a("div",{staticStyle:{margin:"10px",overflow:"hidden"}},[a("div",{staticStyle:{float:"right"}},[a("Page",{attrs:{total:t.table.total,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePage}})],1)]),t._v(" "),a("Modal",{attrs:{"mask-closable":!1,width:"535","class-name":"ma-edit-modal"},model:{value:t.editModal,callback:function(e){t.editModal=e},expression:"editModal"}},[a("div",{staticClass:"edit-modal-body"},[a("Icon",{attrs:{type:"android-close"},on:{click:function(e){t.editModal=!1}}}),t._v(" "),"new"==t.formValidate.type?a("div",{staticClass:"title"},[t._v("新增标签")]):t._e(),t._v(" "),"edit"==t.formValidate.type?a("div",{staticClass:"title"},[t._v("编辑标签")]):t._e(),t._v(" "),a("Form",{ref:"formValidate",attrs:{model:t.formValidate,rules:t.ruleValidate,"label-width":100}},[0!=t.arcCateList.length?a("FormItem",{attrs:{label:"文章爆料类型",prop:"arcCate"}},[a("Select",{model:{value:t.formValidate.arcCate,callback:function(e){t.$set(t.formValidate,"arcCate",e)},expression:"formValidate.arcCate"}},t._l(t.arcCateList,function(e){return a("Option",{key:e.group_id,attrs:{value:e.group_id}},[t._v(t._s(e.group_name))])}))],1):t._e(),t._v(" "),a("FormItem",{attrs:{label:"一级关键词",prop:"first_keywords"}},[a("Input",{attrs:{autosize:"",type:"textarea",placeholder:"关键词之间请用逗号隔开"},model:{value:t.formValidate.first_keywords,callback:function(e){t.$set(t.formValidate,"first_keywords",e)},expression:"formValidate.first_keywords"}})],1),t._v(" "),a("FormItem",{attrs:{label:"二级属性词",prop:"second_keywords"}},[a("Input",{attrs:{autosize:"",type:"textarea",placeholder:"关键词之间请用逗号隔开"},model:{value:t.formValidate.second_keywords,callback:function(e){t.$set(t.formValidate,"second_keywords",e)},expression:"formValidate.second_keywords"}})],1)],1)],1),t._v(" "),a("div",{staticClass:"zhijian-btn-box"},[a("div",{staticClass:"zhijian-btn-confirm",on:{click:function(e){t.submitForm("formValidate")}}},[t._v("确定")])])])],1)},staticRenderFns:[]};var o=a("VU/8")(i,r,!1,function(t){a("StOw")},null,null);e.default=o.exports}});