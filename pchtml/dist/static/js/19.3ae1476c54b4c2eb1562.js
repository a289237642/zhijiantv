webpackJsonp([19],{M7Rz:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var a={name:"bannerManagement",data:function(){var t=this;return{isShow:!1,name:"",path:"",picurl:"",iconid:0,table:{page:1,pagesize:10,total:50,columns:[{title:"序号",key:"id",align:"center",width:100},{title:"名称",key:"name",align:"center",render:function(e,n){return e("input",{attrs:{placeholder:"请输入",value:n.row.name},style:{background:"none",outline:"none",border:"0px",textAlign:"center"},on:{change:function(e){t.name=e.target.value}}})}},{title:"图标",key:"pic",align:"center",render:function(e,n){return e("div",{attrs:{class:"button",for:"inputFile"},on:{click:function(e){t.iconid=n.row.id,document.getElementById("inputFile"+n.row.id).click()}}},[e("img",{attrs:{src:t.iconid==n.row.id?t.picurl:n.row.pic,alt:"上传",class:"iconwidth"}}),e("span",{attrs:{style:""==n.row.pic?"color:#ffc639":"display:none"}},"上传"),e("input",{attrs:{type:"file",id:"inputFile"+n.row.id,style:"display:none;"},on:{change:function(e){var n=t,a=e.target.files||e.dataTransfer.files;if(a.length){var i=e.target.files[0].type;if(/^image/.test(i)){var r=new FileReader;r.readAsDataURL(a[0]),r.onload=function(){(new FormData).append("data",this.result);n.$http.post("/api/v1_0/uploadimage",{type:"jpg",data:this.result}).then(function(t){n.picurl=t.data.url})}}}}}})],t.iconid==n.row.id?t.picurl:"")}},{title:"跳转小程序路径",key:"jump_url",align:"center",render:function(e,n){return e("input",{attrs:{placeholder:"请输入",value:n.row.jump_url},style:{background:"none",outline:"none",border:"0px",textAlign:"center",width:"100%"},on:{change:function(e){t.path=e.target.value}}})}},{title:"操作",align:"center",render:function(e,n){return e("div",[e("button",{attrs:{class:"newbtn zhijian-new-btn"},style:{color:"#fff",borderRadius:"10px",width:"100px",height:"40px",lineHeight:"20px",outline:"none",border:"0px"},on:{click:function(){t.picurl,t.path;var e=t;t.$http.post(t.PATH.UPDATEICON,{icon_id:n.row.id,name:e.name||n.row.name,pic:e.picurl||n.row.pic,jump_url:e.path||n.row.jump_url}).then(function(e){"200"==e.data.status&&t.$Modal.success({width:360,content:e.data.msg,onOk:function(){t.getdata()}})})}}},"提交")])}}],data:[]},h5Img:"",formValidate:{type:"new",row:{},sort:"",status:"1"}}},created:function(){this.getdata()},methods:{getdata:function(){var t=this;this.$http.get(this.PATH.PCICONLIST).then(function(e){200==e.status?0==e.data.errno?t.table.data=e.data.data:t.$Modal.error({width:360,content:e.data.errmsg}):t.$Message.error("Fail!")})}}},i={render:function(){var t=this.$createElement,e=this._self._c||t;return e("div",{attrs:{id:"bannerManagement"}},[e("div",{staticClass:"h1"},[this._v("icon管理")]),this._v(" "),e("Table",{staticClass:"zhijian-table account-table",attrs:{stripe:"",columns:this.table.columns,data:this.table.data}})],1)},staticRenderFns:[]};var r=n("VU/8")(a,i,!1,function(t){n("kvj6")},null,null);e.default=r.exports},kvj6:function(t,e){}});