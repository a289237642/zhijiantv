webpackJsonp([35],{"9oeD":function(t,i,e){"use strict";Object.defineProperty(i,"__esModule",{value:!0});var a={name:"tipoffList",data:function(){var t=this;return{is_search:!1,name0:"name0",paramses:{},modal1:!1,showModal:!1,confirm:"请确认是否取消突出显示",configModal:!1,value:"",group_id:1,onlinelist:[],online:[],onlineid:0,showSort:!1,art_detail:{},detailModal:!1,checkedArc:[],isLoding:!1,table:{total:10,totalAll:10,totalSearch:10,page:1,pagesize:10,is_show:1},formValidate:{sort:"",onlinecategory:""},ruleValidate:{sort:[{required:!0,message:"序号",trigger:"blur"}],content:[{required:!0,message:"请选择上线类型",trigger:"blur"}]},columns1:[{type:"selection",title:"全选",width:50,align:"center"},{title:"排序",key:"sort_num",align:"center",render:function(t,i){return t("div",{style:{textAlign:"center"}},i.row.sort_num)}},{title:"内容",key:"content",width:500,render:function(i,e){return i("div",{style:{display:"flex",alignItems:"center",height:"120px"},on:{click:function(){t.detailModal=!0,t.onlineid=e.row.article_id,t.getDetail()}}},[i("div",{style:{width:"160px",height:"90px",overflow:"hidden",marginRight:"20px",position:"relative"}},[i("img",{attrs:{src:e.row.min_pic},style:{width:"160px"}}),i("i",{attrs:{class:"iconfont icon-audio"},style:{position:"absolute",right:"5px",bottom:"10px",display:"1"==e.row.is_read?"normal":"none"}})]),i("div",{style:{}},[i("p",{style:{fontSize:"18px",color:"#999",width:"300px",overflow:"hidden",textOverflow:"ellipsis",display:"-webkit-box",webkitLineClamp:2,webkitBoxOrient:"vertical"}},e.row.title),i("p",{style:{fontSize:"18px",color:"#999",width:"300px"}},[i("span","转载："),i("span",{style:{color:"blue"}},e.row.author)])])])}},{title:"所属分类",key:"group_name_list",align:"center",render:function(t,i){return t("div",[t("span",{},[i.row.group_name])])}},{title:"上线时间",key:"zj_art_date",align:"center",sortable:!0},{title:"操作",key:"action",align:"center",render:function(i,e){return i("div",[i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"1"==e.row.is_read?"white":"black",border:"1"==e.row.is_read?"1px solid black":"none",color:"1"==e.row.is_read?"black":"white",marginRight:"5px"},on:{click:function(){t.paramses=e,t.onlineid=e.row.article_id,t.$Spin.show({render:function(t){return t("div",[t("Icon",{class:"demo-spin-icon-load",props:{type:"ios-loading",size:18}}),t("div","操作中...")])}}),t.getAudio()}}},"1"==e.row.is_read?"取消音频":"生成音频"),i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"1"==e.row.is_big?"white":"black",border:"1"==e.row.is_big?"1px solid black":"none",color:"1"==e.row.is_big?"black":"white",marginRight:"5px"},on:{click:function(){t.paramses=e,t.confirm="1"==e.row.is_big?"请确认是否取消突出显示":"请确认是否突出显示",t.showModal=!0}}},"1"==e.row.is_big?"取消显示":"突出显示"),i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"black",border:"none",marginRight:"5px"},on:{click:function(){t.paramses=e,t.getgroups(),t.onlineid=e.row.article_id,t.getbelongcate(e.row)}}},"设置"),i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"black",border:"none",marginRight:"30px"},on:{click:function(){t.paramses=e,t.checkedArc.push(e.row.article_id),t.modal1=!0}}},"下线")])}}],columns2:[{type:"selection",title:"全选",width:50,align:"center"},{title:"内容",key:"content",width:500,render:function(i,e){return i("div",{style:{display:"flex",alignItems:"center",height:"120px"},on:{click:function(){t.detailModal=!0,t.onlineid=e.row.article_id,t.getDetail()}}},[i("div",{style:{width:"160px",height:"90px",overflow:"hidden",marginRight:"20px",position:"relative"}},[i("img",{attrs:{src:e.row.min_pic},style:{width:"160px"}}),i("i",{attrs:{class:"iconfont icon-audio"},style:{position:"absolute",right:"5px",bottom:"10px",width:"20px",height:"20px",color:"#fff",zIndex:9,display:"1"==e.row.is_read?"normal":"none"}})]),i("div",{style:{}},[i("p",{style:{fontSize:"18px",color:"#999",width:"300px",overflow:"hidden",textOverflow:"ellipsis",display:"-webkit-box",webkitLineClamp:2,webkitBoxOrient:"vertical"}},e.row.title),i("p",{style:{fontSize:"18px",color:"#999",width:"300px"}},[i("span","转载："),i("span",{style:{color:"blue"}},e.row.author)])])])}},{title:"所属分类",key:"group_name_list",render:function(t,i){return t("div",[t("span",{},i.row.group_name_list+" ")])}},{title:"上线时间",key:"wechat_art_date",sortable:!0},{title:"操作",key:"action",align:"center",render:function(i,e){return i("div",[i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"1"==e.row.is_read?"white":"black",border:"1"==e.row.is_read?"1px solid black":"none",color:"1"==e.row.is_read?"black":"white",marginRight:"5px"},on:{click:function(){t.paramses=e,t.onlineid=e.row.article_id,t.$Spin.show({render:function(t){return t("div",[t("Icon",{class:"demo-spin-icon-load",props:{type:"ios-loading",size:18}}),t("div","操作中...")])}}),t.getAudio()}}},"1"==e.row.is_read?"取消音频":"生成音频"),i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"1"==e.row.is_big?"white":"black",border:"1"==e.row.is_big?"1px solid black":"none",color:"1"==e.row.is_big?"black":"white",marginRight:"5px"},on:{click:function(){t.paramses=e,t.confirm="1"==e.row.is_big?"请确认是否取消突出显示":"请确认是否突出显示",t.showModal=!0}}},"1"==e.row.is_big?"取消显示":"突出显示"),i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"black",border:"none",marginRight:"5px"},on:{click:function(){t.onlineid=e.row.article_id,t.getgroups(),t.getbelongcate(e.row)}}},"设置"),i("Button",{props:{type:"primary",size:"small",class:"btn"},style:{background:"black",border:"none",marginRight:"30px"},on:{click:function(){t.paramses=e,t.checkedArc.push(e.row.article_id),t.modal1=!0}}},"下线")])}}],data1:[],data2:[]}},created:function(){this.getArticlesAll(),this.getgroups()},methods:{getArticlesAll:function(){var t=this;this.$http.post(this.PATH.ARTICLES,{page:this.table.page,pagesize:this.table.pagesize,is_show:1}).then(function(i){200==i.status&&(t.data2=i.data.data,t.table.totalAll=i.data.count)})},getArticles:function(){var t=this;this.$http.post(this.PATH.ARTICLEGROUP,{group_id:this.group_id,page:this.table.page,pagesize:this.table.pagesize}).then(function(i){200==i.status&&(t.data1=i.data.data,t.table.total=i.data.count)})},handTabClick:function(t){this.name0=t,this.is_search=!1,this.group_id=t,this.changePages(),"name0"==t?this.getArticlesAll():this.getArticles()},downlineArc:function(t){var i=this;this.checkedArc=[],t.forEach(function(t){i.checkedArc.push(t.article_id)})},downArc:function(t){var i=this;this.checkedArc=[],t.forEach(function(t){i.checkedArc.push(t.article_id)})},downline1:function(){var t=this,i={},e=this.checkedArc;i="name0"===this.name0?{article_id_list:e}:{article_id_list:e,group_id:this.group_id},this.$http.post(this.PATH.DOWNLINE,i).then(function(i){200==i.status&&(t.$Modal.error({width:360,content:i.data.errmsg}),t.is_search?t.search():"name0"===t.name0?t.getArticlesAll():t.getArticles(),t.checkedArc=[])})},downline:function(){var t=this,i=this.paramses,e={},a=this.checkedArc;e=void 0===i.row.wechat_art_date?{article_id_list:a,group_id:this.group_id}:{article_id_list:a},this.$http.post(this.PATH.DOWNLINE,e).then(function(e){200==e.status&&(t.$Modal.error({width:360,content:e.data.errmsg}),t.is_search?t.search():void 0===i.row.wechat_art_date?t.getArticles():t.getArticlesAll(),t.checkedArc=[])})},showOk:function(){var t,i=this,e=this.paramses.index,a=this.paramses.row.is_big;t={article_id:this.paramses.row.article_id},this.$http.post(this.PATH.SHOWBIG,t).then(function(t){200==t.status&&(i.is_search?i.search():void 0===i.paramses.row.wechat_art_date?i.data1[e].is_big="0"==a?"1":"0":i.data2[e].is_big="0"==a?"1":"0")}),this.showModal=!1},ok:function(){this.modal1=!1,this.downline()},changePages:function(){this.table.page=1},search:function(){var t=this;this.is_search=!0,this.name0="name0",this.$http.post(this.PATH.ONLINESearch,{words:this.value,page:this.table.page,pagesize:this.table.pagesize}).then(function(i){200==i.status&&(t.data2=i.data.data,t.table.totalAll=i.data.count)})},changePage:function(t){this.table.page=t,this.getArticles()},changePageAll:function(t){this.table.page=t,this.is_search?this.search():this.getArticlesAll()},getgroups:function(){var t=this;this.$http.get(this.PATH.PCGROUPS).then(function(i){0==i.data.errno?(t.onlinelist=i.data.data.map(function(t){return{group_id:parseInt(t.group_id.slice(2)),group_name:t.group_name}}),t.online.push(t.group_id)):t.$Modal.error({width:360,content:i.data.errmsg})})},getbelongcate:function(t){var i=this;this.configModal=!0,this.isLoding=!0,this.online=[],this.onlineid=t.article_id,this.$http.post(this.PATH.CURRENTGROUP,{article_id:t.article_id}).then(function(t){if(0==t.data.errno){var e=i;t.data.data.forEach(function(t){e.online.push(t.group_id)}),setTimeout(function(){e.isLoding=!1},600)}else i.$Modal.error({width:360,content:t.data.errmsg})})},configOk:function(){var t=this;this.$http.post(this.PATH.SETARTICLE,{article_id:this.onlineid,group_id_list:this.online}).then(function(i){200==i.status&&(t.$Modal.error({width:360,content:i.data.errmsg}),t.is_search?t.search():void 0===t.paramses.row.wechat_art_date?t.getArticles():t.getArticlesAll())}),this.configModal=!1,this.formValidate.sort=""},getDetail:function(){var t=this;this.art_detail={},this.$http.post(this.PATH.ARTICLEDETAILS,{article_id:this.onlineid}).then(function(i){0==i.data.errno?t.art_detail=i.data.data:t.$Modal.error({width:360,content:i.data.errmsg})})},getAudio:function(){var t=this,i=this.paramses.index,e=this.paramses.row.is_read,a=[];a.push(this.onlineid),this.$http.post(this.PATH.GETAUDIO,{article_id_list:a,is_read:e}).then(function(a){200==a.status&&(t.$Spin.hide(),t.$Message.info(a.data.errmsg),0==a.data.errno&&(t.is_search?t.search():void 0===t.paramses.row.wechat_art_date?t.data1[i].is_read="1"==e?"0":"1":t.data2[i].is_read="1"==e?"0":"1"))})},getMoreAudio:function(){var t=this;this.$http.post(this.PATH.GETAUDIO,{article_id_list:this.checkedArc}).then(function(i){200==i.status&&(t.$Spin.hide(),t.$Message.info(i.data.errmsg),0==i.data.errno&&(t.is_search?t.search():"name0"===t.name0?t.getArticlesAll():t.getArticles(),t.checkedArc=[]))})}}},o={render:function(){var t=this,i=t.$createElement,e=t._self._c||i;return e("div",{attrs:{id:"tipoffList"}},[e("h1",[t._v("爆料列表")]),t._v(" "),e("Input",{staticClass:"search",attrs:{search:"","enter-button":"搜索",placeholder:"请输入搜索关键字"},on:{"on-search":t.search,"on-blur":t.changePages},model:{value:t.value,callback:function(i){t.value=i},expression:"value"}}),t._v(" "),e("Button",{staticClass:"newbtn1 zhijian-new-btn",attrs:{type:"primary"},on:{click:t.getMoreAudio}},[t._v("批量生成音频")]),t._v(" "),e("Button",{staticClass:"newbtn zhijian-new-btn",attrs:{type:"primary"},on:{click:t.downline1}},[t._v("批量下线")]),t._v(" "),e("Tabs",{attrs:{value:t.name0},on:{"on-click":t.handTabClick}},[e("TabPane",{attrs:{label:"全部",name:"name0"}},[e("Table",{ref:"selection",staticClass:"tip-table",attrs:{border:"",columns:t.columns2,data:t.data2},on:{"on-selection-change":t.downArc,"on-select-all":t.downlineArc}}),t._v(" "),e("div",{staticClass:"zhijian-pagination"},[e("Page",{attrs:{total:t.table.totalAll,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePageAll}})],1)],1),t._v(" "),t._l(t.onlinelist,function(i){return e("TabPane",{key:i.group_id,attrs:{label:i.group_name,name:i.group_id+"",value:i.group_id}},[e("Table",{ref:"selection",refInFor:!0,staticClass:"tip-table",attrs:{border:"",columns:t.columns1,data:t.data1},on:{"on-selection-change":t.downArc,"on-select-all":t.downlineArc}}),t._v(" "),e("div",{staticClass:"zhijian-pagination"},[e("Page",{attrs:{total:t.table.total,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePage}})],1)],1)})],2),t._v(" "),e("Modal",{attrs:{title:"Common Modal dialog box title"},model:{value:t.showModal,callback:function(i){t.showModal=i},expression:"showModal"}},[e("p",{staticClass:"modelp"},[t._v(t._s(t.confirm))]),t._v(" "),e("div",{staticClass:"zhijian-btn-box"},[e("div",{staticClass:"zhijian-btn-confirm",on:{click:t.showOk}},[t._v("确定")])])]),t._v(" "),e("Modal",{attrs:{title:"Common Modal dialog box title","class-name":"ma-edit-modal"},model:{value:t.configModal,callback:function(i){t.configModal=i},expression:"configModal"}},[e("div",{staticClass:"edit-modal-body"},[e("Icon",{attrs:{type:"android-close"},on:{click:function(i){t.editModal=!1}}}),t._v(" "),e("div",{staticClass:"title"},[t._v("设置")]),t._v(" "),e("Form",{ref:"formValidate",attrs:{model:t.formValidate,rules:t.ruleValidate,"label-width":100}},[e("FormItem",{attrs:{label:"上线类型",prop:"onlinecategory"}},[e("Select",{attrs:{filterable:"",multiple:""},model:{value:t.online,callback:function(i){t.online=i},expression:"online"}},t._l(t.onlinelist,function(i){return e("Option",{key:i.group_id,attrs:{value:i.group_id}},[t._v(t._s(i.group_name))])}))],1)],1)],1),t._v(" "),e("div",{staticClass:"zhijian-btn-box"},[e("div",{staticClass:"zhijian-btn-confirm",on:{click:t.configOk}},[t._v("确定")])]),t._v(" "),e("Col",{directives:[{name:"show",rawName:"v-show",value:t.isLoding,expression:"isLoding"}],staticClass:"demo-spin-col",attrs:{span:"8"}},[e("Spin",{attrs:{size:"large"}})],1)],1),t._v(" "),e("Modal",{attrs:{title:"Common Modal dialog box title"},model:{value:t.modal1,callback:function(i){t.modal1=i},expression:"modal1"}},[e("p",{staticClass:"modelp"},[t._v("请确认该文章是否下线")]),t._v(" "),e("div",{staticClass:"zhijian-btn-box"},[e("div",{staticClass:"zhijian-btn-confirm",on:{click:t.ok}},[t._v("确定")])])]),t._v(" "),e("Modal",{attrs:{title:"Common Modal dialog box title",width:"735"},model:{value:t.detailModal,callback:function(i){t.detailModal=i},expression:"detailModal"}},[e("div",{staticClass:"detail"},[e("h1",[t._v(t._s(t.art_detail.title))]),t._v(" "),e("div",{staticClass:"come-from"},[e("span",[t._v("转载："+t._s(t.art_detail.author))]),t._v(" "),e("span",[t._v(t._s(t.art_detail.wechat_art_date))])]),t._v(" "),t._l(t.art_detail.content,function(i,a){return e("div",{key:a},[i.text?e("p",{staticClass:"cont-text"},[t._v(t._s(i.text))]):e("img",{staticClass:"cont-img",attrs:{mode:"aspectFit",src:i.img,alt:""}})])})],2)])],1)},staticRenderFns:[]};var s=e("VU/8")(a,o,!1,function(t){e("xOJc")},null,null);i.default=s.exports},xOJc:function(t,i){}});