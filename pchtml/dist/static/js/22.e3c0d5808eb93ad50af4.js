webpackJsonp([22],{N5VL:function(a,t){},pwiO:function(a,t,e){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var i={name:"goodsList",data:function(){var a=this;return{isOn:"上架",tagid:"",name:"name1",is_search:!1,searchValue:"",model:"",goodsid:1,val:"",page:1,pagesize:10,total:50,modal1:!1,modal2:!1,categoryList:[{name:"全部分类"}],allColumns:[{title:"商品描述",key:"goods_name",width:300,render:function(a,t){return a("div",[a("img",{attrs:{src:t.row.min_pic},style:{width:"100px",height:"70px",border:"1px solid",marginRight:"20px",verticalAlign:"middle",marginTop:"10px"}}),a("p",{style:{width:"160px",height:"55px",marginTop:"-65px",marginLeft:"120px",overflow:"hidden",marginBottom:"20px"}},t.row.goods_name)])}},{title:"已兑换",key:"change_num",align:"center"},{title:"库存",key:"ku_num",align:"center"},{title:"创建时间",key:"create_time",width:200,align:"center"},{title:"下单名单",key:"nameList",align:"center",render:function(t,e){return t("div",[t("Icon",{props:{type:"ios-list-box-outline",size:32},style:{textAlign:"center"},on:{click:function(){a.$router.push({name:"applicationLists",params:{goodsid:e.row.goods_id}})}}})])}},{title:"操作",key:"action",width:300,align:"center",render:function(t,e){var i="下架",s="#FFC639",o="#fff";return 1==e.row.is_show?(i="下架",s="#fff",o="#000"):(s="#FFC639",i="上架",o="#fff"),t("div",[t("Button",{props:{type:"primary",size:"small"},style:{color:o,marginRight:"5px",background:s,borderColor:"#FFC639"},on:{click:function(){a.isOn=i,a.modal1=!0,a.goodsid=e.row.goods_id}}},i),t("Icon",{props:{type:"ios-create-outline",size:32},style:{marginRight:"5px"},on:{click:function(){a.$router.push({name:"addGoods",query:{isEdit:!0,goodsid:e.row.goods_id}})}}}),t("Icon",{props:{type:"ios-trash-outline",size:32},style:{marginRight:"5px"},on:{click:function(){a.goodsid=e.row.goods_id,a._data.modal2=!0}}})])}}],allData:[]}},created:function(){this.getData()},methods:{getData:function(){var a=this,t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,e={};1===t?e={page:this.page,pagesize:this.pagesize,is_show:1}:-1===t?e={page:this.page,pagesize:this.pagesize,is_show:-1}:0===t&&(e={page:this.page,pagesize:this.pagesize}),this.$http.post(this.PATH.GOODSLIST,e).then(function(t){0==t.data.errno?(a.allData=t.data.data,a.total=t.data.count):a.$Modal.error({width:360,content:t.data.errmsg})})},changeTabs:function(a){this.page=1,this.is_search=!1,"name1"==a?this.getData():"name2"==a?this.getData(1):this.getData(-1),this.name=a},getDataAll:function(){"name1"==this.name?this.getData():"name2"==this.name?this.getData(1):this.getData(-1)},getClassify:function(a){var t="";this.categoryList.forEach(function(e){"全部分类"===a?t="":a==e.name&&(t=e.id)}),this.tagid=t,this.getSearchDataAll(this.searchValue)},changePage:function(a){this.page=a,this.is_search?this.getSearchDataAll(this.searchValue):this.getDataAll()},okIsOn:function(){var a=this;this.$http.post(this.PATH.GOODSDOWN,{goods_id:this.goodsid}).then(function(t){a.modal1=!1,0===t.data.errno&&a.getDataAll()})},okIsDelete:function(){var a=this;this.$http.post(this.PATH.GOODSDEL,{goods_id:this.goodsid}).then(function(t){0===t.data.errno&&(a.modal2=!1,a.getDataAll())})},cancel:function(){this.modal1=!1,this.modal2=!1},addGoods:function(){this.$router.push({name:"addGoods"})},getSearchDataAll:function(a){"name1"==this.name?this.getSearchList(a):"name2"==this.name?this.getSearchList(a,-1):this.getSearchList(a,1)},getSearchList:function(a,t){var e=this;this.$http.post(this.PATH.GOODSQUERY,{goods_name:a,page:e.page,pagesize:10,is_show:t}).then(function(a){0===a.data.errno&&(e.allData=a.data.data,e.total=a.data.count)})},getSearchValue:function(a){this.is_search=!0,this.page=1,this.searchValue=a,this.getSearchDataAll(this.searchValue)}}},s={render:function(){var a=this,t=a.$createElement,e=a._self._c||t;return e("div",{attrs:{id:"goodsList"}},[e("div",{staticClass:"h1"},[a._v("商品列表")]),a._v(" "),e("div",{staticClass:"header"},[e("Input",{staticClass:"search",attrs:{search:"","enter-button":"搜索",placeholder:"快速搜索","v-model":a.val},on:{"on-search":a.getSearchValue}}),a._v(" "),e("Button",{staticClass:"newbtn zhijian-new-btn",attrs:{type:"primary"},on:{click:a.addGoods}},[a._v("新增")])],1),a._v(" "),e("Tabs",{staticClass:"tabs",attrs:{value:"name1",size:"default"},on:{"on-click":a.changeTabs}},[e("TabPane",{staticClass:"tabpane",attrs:{label:"全部",name:"name1"}},[e("Table",{attrs:{data:a.allData,columns:a.allColumns,stripe:""}}),a._v(" "),e("Modal",{attrs:{draggable:"",scrollable:"","class-name":"modal"},model:{value:a.modal1,callback:function(t){a.modal1=t},expression:"modal1"}},[e("div",[a._v("请确认是否"+a._s(a.isOn)+"商品")]),a._v(" "),e("div",{staticClass:"cancle",on:{click:a.cancel}},[a._v("取消")]),a._v(" "),e("div",{staticClass:"zhijian-btn-confirm",on:{click:a.okIsOn}},[a._v("确定")])]),a._v(" "),e("Modal",{attrs:{draggable:"",scrollable:""},model:{value:a.modal2,callback:function(t){a.modal2=t},expression:"modal2"}},[e("div",[a._v("请确认是否删除商品")]),a._v(" "),e("div",{staticClass:"cancle",on:{click:a.cancel}},[a._v("取消")]),a._v(" "),e("div",{staticClass:"zhijian-btn-confirm",on:{click:a.okIsDelete}},[a._v("确定")])]),a._v(" "),e("div",{staticStyle:{margin:"10px",overflow:"hidden"}},[e("div",{staticStyle:{float:"right"}},[e("Page",{attrs:{total:a.total,current:a.page,"show-elevator":"",pageSize:a.pagesize},on:{"on-change":a.changePage}})],1)])],1),a._v(" "),e("TabPane",{staticClass:"tabpane",attrs:{label:"进行中",name:"name2"}},[e("Table",{attrs:{data:a.allData,columns:a.allColumns,stripe:""}}),a._v(" "),e("Modal",{attrs:{draggable:"",scrollable:"",title:"Modal 1"},model:{value:a.modal1,callback:function(t){a.modal1=t},expression:"modal1"}},[e("div",[a._v("请确认是否下架商品")])]),a._v(" "),e("Modal",{attrs:{draggable:"",scrollable:"",title:"Modal 2"},model:{value:a.modal2,callback:function(t){a.modal2=t},expression:"modal2"}},[e("div",[a._v("请确认是否删除商品")])]),a._v(" "),e("div",{staticStyle:{margin:"10px",overflow:"hidden"}},[e("div",{staticStyle:{float:"right"}},[e("Page",{attrs:{total:a.total,current:a.page,"show-elevator":"",pageSize:a.pagesize},on:{"on-change":a.changePage}})],1)])],1),a._v(" "),e("TabPane",{staticClass:"tabpane",attrs:{label:"已下架",name:"name3"}},[e("Table",{attrs:{data:a.allData,columns:a.allColumns,stripe:""}}),a._v(" "),e("Modal",{attrs:{draggable:"",scrollable:"",title:"Modal 1"},model:{value:a.modal1,callback:function(t){a.modal1=t},expression:"modal1"}},[e("div",[a._v("请确认是否"+a._s(a.isOn)+"商品")])]),a._v(" "),e("Modal",{attrs:{draggable:"",scrollable:"",title:"Modal 2"},model:{value:a.modal2,callback:function(t){a.modal2=t},expression:"modal2"}},[e("div",[a._v("请确认是否删除商品")])]),a._v(" "),e("div",{staticStyle:{margin:"10px",overflow:"hidden"}},[e("div",{staticStyle:{float:"right"}},[e("Page",{attrs:{total:a.total,current:a.page,"show-elevator":"",pageSize:a.pagesize},on:{"on-change":a.changePage}})],1)])],1)],1)],1)},staticRenderFns:[]};var o=e("VU/8")(i,s,!1,function(a){e("N5VL")},null,null);t.default=o.exports}});