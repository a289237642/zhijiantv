webpackJsonp([26],{"73Kn":function(t,a){},"w2/H":function(t,a,e){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var i={name:"dataOverview",data:function(){var t=this;return{isShow:!1,editModal:!1,is_search:!1,searchValue:"",table:{page:1,pagesize:10,total:50,columns:[{title:"序号",key:"location",align:"center",width:150},{title:"渠道名称",key:"spread_name",align:"center"},{title:"授权用户总数",key:"auth_num",align:"center"},{title:"首次访问用户总数",key:"not_auth_num",align:"center"},{title:"操作",align:"center",render:function(a,e){return a("div",[a("Button",{props:{type:"primary",size:"small"},style:{marginRight:"5px"},on:{click:function(){t.goToDetail(e.row)}}},"详情")])}}],data:[]}}},created:function(){this.getdata(this.table.page,this.table.pagesize)},methods:{getdata:function(t,a){var e=this;this.$http.post(this.PATH.SPREADDATALS,{page:t,pagesize:a}).then(function(t){200==t.status?0==t.data.errno?(e.table.data=t.data.data,e.table.total=t.data.count):e.$Modal.error({width:360,content:t.data.errmsg}):e.$Message.error("Fail!")})},changePage:function(t){this.table.page=t,this.is_search?this.getSearch():this.getdata(t,this.table.pagesize)},goToDetail:function(t){this.$router.push({name:"spreadDetail",query:{id:t.spread_id}})},getSearch:function(){var t=this;this.is_search=!0,this.$http.post(this.PATH.SPREADDATASEARCH,{page:this.table.page,pagesize:this.table.pagesize,words:this.searchValue}).then(function(a){200==a.status?0==a.data.errno?(t.table.data=a.data.data,t.table.total=a.data.count):t.$Modal.error({width:360,content:a.data.errmsg}):t.$Message.error("Fail!")})}}},n={render:function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{attrs:{id:"dataOverview"}},[e("div",{staticClass:"h1"},[t._v("数据概览")]),t._v(" "),e("div",{staticClass:"header"},[e("Input",{staticClass:"search",attrs:{search:"","enter-button":"搜索",placeholder:"快速搜索"},on:{"on-search":t.getSearch,"on-blur":function(a){t.table.page=1},"on-enter":function(a){t.table.page=1}},model:{value:t.searchValue,callback:function(a){t.searchValue=a},expression:"searchValue"}})],1),t._v(" "),e("Table",{staticClass:"zhijian-table account-table",attrs:{stripe:"",columns:t.table.columns,data:t.table.data}}),t._v(" "),e("div",{staticClass:"zhijian-pagination"},[e("Page",{attrs:{total:t.table.total,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePage}})],1)],1)},staticRenderFns:[]};var s=e("VU/8")(i,n,!1,function(t){e("73Kn")},null,null);a.default=s.exports}});