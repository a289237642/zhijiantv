webpackJsonp([17],{"DG/P":function(t,e,a){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i={name:"tipoffList",data:function(){var t=this;return{editModal:!1,moveModal:!1,animal:"1",title:"",name:"",delemodal:!1,startDate:"",h5Img:"",h5Img1:"",h5Img2:"",audiopath:"",endDate:"",endtime:"",name0:"name0",paramses:{},is_show:1,isShow:!0,audioid:1,lessonid:this.$route.params.lessonid,deatillesson:{},detailModal:!1,checkedLesson:[],ishowFile:!0,table:{total:10,totalAll:10,totalSearch:10,page:1,pagesize:10,is_show:1},formValidate:{type:"new",cost_type:"1"},ruleValidate:{title:[{required:!0,message:"标题",trigger:"blur"}],cost_type:[{required:!0,message:"请选择支付类型",trigger:"blur"}]},formValidate1:{type:"new",cost_type:"1"},ruleValidate1:{title:[{required:!0,message:"标题",trigger:"blur"}],cost_type:[{required:!0,message:"请选择支付类型",trigger:"blur"}]},columns2:[{type:"selection",title:"全选",width:60,align:"center",key:"id"},{title:"序号",key:"location",width:100},{title:"名称",key:"name",align:"center",width:200,render:function(e,a){return e("input",{attrs:{placeholder:"请输入",value:a.row.name},style:{background:"none",outline:"none",border:"0px",textAlign:"center"},on:{change:function(e){t.name=e.target.value}}})}},{title:"标题",key:"title",align:"center",width:200,render:function(e,a){return e("input",{attrs:{placeholder:"请输入",value:a.row.title},style:{background:"none",outline:"none",border:"0px",textAlign:"center"},on:{change:function(e){t.title=e.target.value}}})}},{title:"音频文件",key:"pic",align:"center",width:400,render:function(e,a){return e("div",[e("Icon",{attrs:{type:"md-cloud-upload",size:"20",style:""==a.row.mp3_url?"":"display:none;"},on:{click:function(){document.getElementById("inputFile1").click()}}}),e("span",{attrs:{type:"md-cloud-upload",size:"20"},on:{click:function(){t.audioid=a.row.id,document.getElementById("inputFile1").click()}}},t.audioid==a.row.id?t.audiopath:a.row.mp3_url),e("input",{attrs:{type:"file",id:"inputFile1",style:"display:none;"},on:{change:function(e){var a=t;if((e.target.files||e.dataTransfer.files).length){var i=new FormData;i.append("file",e.target.files[0]);t.$Spin.show({render:function(t){return t("div",[t("Icon",{class:"demo-spin-icon-load",props:{type:"ios-loading",size:18}}),t("div","上传中...")])}}),a.$http.post("/api/v1_0/upload_audio",i).then(function(t){"0"==t.data.errno?(a.isShow=!0,a.audiopath=t.data.mp3_url,a.$Spin.hide()):a.$Modal.error({title:"提示",content:t.data.errmsg})},function(e){t.$Modal.error({title:"提示",content:success.data.msg})})}}}})])}},{title:"操作",key:"action",align:"center",render:function(e,a){return e("div",[e("Button",{props:{type:"primary",size:"normal",class:"btn"},style:{background:"black",border:"none",marginRight:"5px",display:"1"==a.row.is_show?"none":""},on:{click:function(){t.delemodal=!0,t.paramses=a}}},"删除"),e("Button",{props:{type:"primary",size:"normal",class:"btn"},style:{background:"black",border:"none",marginRight:"5px",display:"0"==a.row.is_show?"none":""},on:{click:function(){t.paramses=a,t.moveModal=!0}}},"移动"),e("Button",{props:{type:"primary",size:"normal",class:"btn"},style:{background:"black",border:"none",marginRight:"30px",display:"0"==a.row.is_show?"none":""},on:{click:function(){t.paramses=a,t.$http.post(t.PATH.ADDLESSONAUDIO,{audio_id:a.row.id,lesson_id:t.$route.params.lessonid,title:t.title||a.row.title,name:t.name||a.row.name,mp3_url:t.audiopath||a.row.mp3_url}).then(function(e){t.formValidate.type,t.$Modal.success({title:"提示",content:e.data.errmsg,onOk:function(){t.editModal=!1}}),t.table.page=1,t.getLessonsAudio()})}}},"提交")])}}],columns3:[{title:"序号",key:"index",align:"center",width:100},{title:"昵称",key:"nick_name",align:"center",width:200},{title:"头像",key:"pic",align:"center",width:400,render:function(t,e){return t("div",{attrs:{class:"button",for:"inputFile"},on:{click:function(t){}}},[t("img",{attrs:{src:e.row.user_img,width:"40px",height:"40px"}})])}},{title:"鼓励值",key:"help_num",align:"center"},{title:"是否已领课程",key:"is_pay",align:"center",render:function(t,e){return t("div",{attrs:{class:"button",for:"inputFile"},on:{click:function(t){}}},[t("p",{attrs:{}},0==e.row.is_pay?"否":"是")])}}],data2:[],data3:[]}},created:function(){this.getLessondetail(),this.getLessonsAudio()},methods:{getLessonsAudio:function(){var t=this;this.$http.post(this.PATH.LESSONAUDIOLIST,{page:this.table.page,pagesize:this.table.pagesize,lesson_id:this.$route.params.lessonid}).then(function(e){200==e.status?0==e.data.errno?(t.data2=e.data.data,t.table.totalAll=e.data.count):t.$Modal.error({width:360,content:e.data.errmsg}):t.$Message.error("Fail!")})},getjoinuser:function(){var t=this;this.$http.post(this.PATH.LESSONPERSONS,{page:this.table.page,pagesize:this.table.pagesize,lesson_id:this.$route.params.lessonid}).then(function(e){200==e.status&&(t.data3=e.data.data,t.table.totalAll=e.data.count)})},getLessondetail:function(){var t=this;this.$http.post(this.PATH.PCLESSONDETAIL,{lesson_id:this.$route.params.lessonid}).then(function(e){200==e.status?0==e.data.errno?(t.deatillesson=e.data.data,t.formValidate.title=t.deatillesson.title,t.formValidate.subtitle=t.deatillesson.subtitle,t.h5Img=t.deatillesson.min_pic,t.formValidate.count=t.deatillesson.count,t.h5Img1=t.deatillesson.summary,t.endDate=t.deatillesson.end_time,t.cost_type=t.deatillesson.cost_type,t.formValidate.present_num=t.deatillesson.present_num,t.formValidate.base_num=t.deatillesson.base_num,t.formValidate.price=t.deatillesson.price,t.lessonid=t.deatillesson.id,t.formValidate.total_audio_num=t.deatillesson.total_audio_num):t.$Modal.success({title:"提示",content:e.data.errmsg}):t.$Message.error("Fail!")})},handTabClick:function(t){this.name0=t,this.is_search=!1,this.group_id=t,"name0"==t?this.getLessonsAudio():"name1"==t?this.getLessondetail():this.getjoinuser()},showEditModal:function(){this.editModal=!0,this.ishowFile=!0},onUpload:function(t){var e=t.target.files||t.dataTransfer.files;if(e.length){t.target.files[0].type;var a=new FileReader;a.readAsDataURL(e[0]);var i=this;a.onload=function(t){var e=this;(new FormData).append("data",this.result);i.$http.post("/api/v1_0/uploadimage",{type:"jpg",data:this.result}).then(function(t){"0"==t.data.status?(i.isShow=!0,i.h5Img=t.data.url):i.$Modal.error({title:"提示",content:t.data.msg})},function(t){e.$Modal.error({title:"提示",content:success.data.msg})})}}},onUpload1:function(t){var e=t.target.files||t.dataTransfer.files;if(e.length){t.target.files[0].type;var a=new FileReader;a.readAsDataURL(e[0]);var i=this;a.onload=function(t){var e=this;(new FormData).append("data",this.result);i.$http.post("/api/v1_0/uploadimage",{type:"jpg",data:this.result}).then(function(t){"0"==t.data.status?(i.isShow=!0,i.h5Img1=t.data.url):i.$Modal.error({title:"提示",content:t.data.msg})},function(t){e.$Modal.error({title:"提示",content:success.data.msg})})}}},onUpload3:function(t){var e=this;this.audiopath="";var a=this;if((t.target.files||t.dataTransfer.files).length){var i=new FormData;i.append("file",t.target.files[0]);this.$Spin.show({render:function(t){return t("div",[t("Icon",{class:"demo-spin-icon-load",props:{type:"ios-loading",size:18}}),t("div","上传中...")])}}),a.$http.post("/api/v1_0/upload_audio",i).then(function(t){"0"==t.data.errno?(a.isShow=!0,a.audiopath=t.data.mp3_url,a.$Spin.hide(),a.ishowFile=!1):a.$Modal.error({title:"提示",content:t.data.errmsg})},function(t){e.$Modal.error({title:"提示",content:success.data.msg})}),this.getLessonsAudio()}},getenddate:function(t){this.endDate=t},submitForm:function(t){var e=this;this.$refs[t].validate(function(t){if(t){var a,i=new Object;a=e.PATH.EDITLESSON,i={lesson_id:e.$route.params.lessonid,title:e.formValidate.title,subtitle:e.formValidate.subtitle,author:sessionStorage.getItem("username"),min_pic:e.h5Img,count:e.formValidate.count,summary:e.h5Img1,end_time:e.endDate,cost_type:1,present_num:e.formValidate.present_num,base_num:e.formValidate.base_num,price:e.formValidate.price,total_audio_num:e.formValidate.total_audio_num},e.$http.post(a,i).then(function(t){e.$Modal.success({title:"提示",content:t.data.errmsg,onOk:function(){e.editModal=!1}}),e.table.page=1})}else e.$Message.error("Fail!")})},submitForm1:function(t){var e=this;this.$refs[t].validate(function(t){if(t){var a=e.formValidate1.type,i="",o=new Object;"new"==a&&(i=e.PATH.ADDLESSONAUDIO,o={lesson_id:e.$route.params.lessonid,title:e.formValidate1.title,name:e.formValidate1.name,mp3_url:e.audiopath}),e.$http.post(i,o).then(function(t){e.$Modal.success({title:"提示",content:t.data.errmsg,onOk:function(){e.editModal=!1,e.audiopath="",e.$refs.formValidate.resetFields(),e.formValidate1.title="",e.formValidate1.name="",e.ishowFile=!1}}),e.table.page=1,e.getLessonsAudio()})}else e.$Message.error("Fail!")})},downlinelesson:function(t){var e=this;this.checkedLesson=[],t.forEach(function(t){e.checkedLesson.push(t.id)})},downlesson:function(t){var e=this;this.checkedLesson=[],t.forEach(function(t){e.checkedLesson.push(t.id)})},deleteOk:function(){var t=this,e=[];0==this.checkedLesson.length?e.push(this.paramses.row.id):e=this.checkedLesson,this.$http.post(this.PATH.DELLESSONAUDIN,{audio_id_list:e,lesson_id:this.$route.params.lessonid}).then(function(e){0==e.data.errno?(t.$Modal.error({width:360,content:e.data.errmsg}),t.getLessonsAudio()):t.$Modal.error({width:360,content:e.data.errmsg})}),this.delemodal=!1},changePageAll:function(t){this.table.page=t,this.getLessonsAudio()},moveOk:function(){var t=this;this.$http.post(this.PATH.AUDIOMOVE,{lesson_id:this.$route.params.lessonid,sort_num:this.paramses.row.sort_num,move:parseInt(this.animal),audio_id:this.paramses.row.id}).then(function(e){200==e.status&&(t.$Modal.error({width:360,content:e.data.errmsg}),t.getLessonsAudio())}),this.moveModal=!1}}},o={render:function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{attrs:{id:"tipoffList"}},[a("h1",[t._v("课程音频列表")]),t._v(" "),a("Tabs",{attrs:{value:t.name0},on:{"on-click":t.handTabClick}},[a("TabPane",{attrs:{label:"课程信息",name:"name0"}},[a("div",{staticClass:"edit-modal-body"},[a("Icon",{attrs:{type:"android-close"},on:{click:function(e){t.editModal=!1}}}),t._v(" "),a("Form",{ref:"formValidate",attrs:{model:t.formValidate,rules:t.ruleValidate,"label-width":100}},[a("FormItem",{attrs:{label:"头图",prop:"min_pic"}},[t.isShow?a("div",{staticClass:"h5ImgBox"},[a("img",{staticStyle:{width:"98px",height:"98px"},attrs:{src:t.h5Img}})]):t._e(),t._v(" "),a("div",[a("label",{staticClass:"button",attrs:{for:"inputFile"}},[a("span",{staticClass:"upload__select"},[t._v("点击上传图片")])])])]),t._v(" "),a("FormItem",{attrs:{label:"商品标题",prop:"title"}},[a("Input",{attrs:{placeholder:"请输入30字以内"},model:{value:t.formValidate.title,callback:function(e){t.$set(t.formValidate,"title",e)},expression:"formValidate.title"}})],1),t._v(" "),a("FormItem",{attrs:{label:"副标题",prop:"subtitle"}},[a("Input",{attrs:{placeholder:"请输入30字以内"},model:{value:t.formValidate.subtitle,callback:function(e){t.$set(t.formValidate,"subtitle",e)},expression:"formValidate.subtitle"}})],1),t._v(" "),a("FormItem",{attrs:{label:"关于课程"}},[t.isShow?a("div",{staticClass:"h5ImgBox"},[a("img",{staticStyle:{width:"98px",height:"98px"},attrs:{src:t.h5Img1}})]):t._e(),t._v(" "),a("div",[a("label",{staticClass:"button",attrs:{for:"inputFile1"}},[a("span",{staticClass:"upload__select"},[t._v("点击上传图片")])])])]),t._v(" "),a("FormItem",{attrs:{label:"课程音频总数",prop:"total_audio_num"}},[a("Input",{attrs:{placeholder:"请输入数字"},model:{value:t.formValidate.total_audio_num,callback:function(e){t.$set(t.formValidate,"total_audio_num",e)},expression:"formValidate.total_audio_num"}})],1),t._v(" "),a("FormItem",{attrs:{label:"支付方式",prop:"cost_type"}},[a("RadioGroup",{model:{value:t.formValidate.cost_type,callback:function(e){t.$set(t.formValidate,"cost_type",e)},expression:"formValidate.cost_type"}},[a("Radio",{attrs:{label:"1"}},[t._v("集赞兑换")])],1)],1),t._v(" "),a("FormItem",{attrs:{label:"集赞数"}},[a("Input",{attrs:{placeholder:"请输入整数数值"},model:{value:t.formValidate.price,callback:function(e){t.$set(t.formValidate,"price",e)},expression:"formValidate.price"}})],1),t._v(" "),a("FormItem",{attrs:{label:"拉新赠送数"}},[a("Input",{attrs:{placeholder:"请输入整数数值"},model:{value:t.formValidate.present_num,callback:function(e){t.$set(t.formValidate,"present_num",e)},expression:"formValidate.present_num"}})],1),t._v(" "),a("FormItem",{attrs:{label:"活动到期时间"}},[a("DatePicker",{staticStyle:{width:"120px"},attrs:{type:"date",placeholder:"到期时间"},on:{"on-change":t.getenddate},model:{value:t.endDate,callback:function(e){t.endDate=e},expression:"endDate"}})],1),t._v(" "),a("FormItem",{attrs:{label:"课程库存"}},[a("Input",{attrs:{placeholder:"请输入整数数值"},model:{value:t.formValidate.count,callback:function(e){t.$set(t.formValidate,"count",e)},expression:"formValidate.count"}})],1),t._v(" "),a("FormItem",{attrs:{label:"领取人数基数"}},[a("Input",{attrs:{placeholder:"0"},model:{value:t.formValidate.base_num,callback:function(e){t.$set(t.formValidate,"base_num",e)},expression:"formValidate.base_num"}})],1),t._v(" "),a("FormItem",{attrs:{label:""}},[a("div",{staticClass:"zhijian-btn-box"},[a("div",{staticClass:"zhijian-btn-confirm",on:{click:function(e){t.submitForm("formValidate")}}},[t._v("修改")])])])],1)],1)]),t._v(" "),a("TabPane",{attrs:{label:"课程音频",name:"name1"}},[a("Button",{staticClass:"audiobtn zhijian-new-btn",attrs:{type:"primary"},on:{click:function(e){t.showEditModal("new")}}},[t._v("新增")]),t._v(" "),a("Button",{staticClass:"audiobtn zhijian-new-btn",attrs:{type:"primary"},on:{click:t.deleteOk}},[t._v("批量删除")]),t._v(" "),a("Table",{ref:"selection",staticClass:"tip-table",attrs:{border:"",columns:t.columns2,data:t.data2},on:{"on-selection-change":t.downlesson,"on-select-all":t.downlinelesson}}),t._v(" "),a("div",{staticClass:"zhijian-pagination"},[a("Page",{attrs:{total:t.table.totalAll,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePageAll}})],1)],1),t._v(" "),a("TabPane",{attrs:{label:"参与用户",name:"name2"}},[a("Table",{ref:"selection",staticClass:"tip-table",attrs:{border:"",columns:t.columns3,data:t.data3},on:{"on-selection-change":t.downlesson,"on-select-all":t.downlinelesson}}),t._v(" "),a("div",{staticClass:"zhijian-pagination"},[a("Page",{attrs:{total:t.table.totalAll,current:t.table.page,"show-elevator":"",pageSize:t.table.pagesize},on:{"on-change":t.changePageAll}})],1)],1)],1),t._v(" "),a("Modal",{attrs:{"mask-closable":!1,width:"935","class-name":"ma-edit-modal"},model:{value:t.editModal,callback:function(e){t.editModal=e},expression:"editModal"}},[a("div",{staticClass:"edit-modal-body"},[a("Icon",{attrs:{type:"android-close"},on:{click:function(e){t.editModal=!1}}}),t._v(" "),"new"==t.formValidate1.type?a("div",{staticClass:"title",staticStyle:{"font-size":"24px",color:"var(--base)","text-align":"center"}},[t._v("新增课程音频")]):t._e(),t._v(" "),a("Form",{ref:"formValidate1",attrs:{model:t.formValidate1,rules:t.ruleValidate1,"label-width":100}},[a("FormItem",{attrs:{label:"名称",prop:"name"}},[a("Input",{attrs:{placeholder:"请输入30字以内"},model:{value:t.formValidate1.name,callback:function(e){t.$set(t.formValidate1,"name",e)},expression:"formValidate1.name"}})],1),t._v(" "),a("FormItem",{attrs:{label:"标题",prop:"title"}},[a("Input",{attrs:{placeholder:"请输入30字以内"},model:{value:t.formValidate1.title,callback:function(e){t.$set(t.formValidate1,"title",e)},expression:"formValidate1.title"}})],1),t._v(" "),a("FormItem",{attrs:{label:"url",prop:"url"}},[a("Input",{attrs:{placeholder:"请输入url"},model:{value:t.audiopath,callback:function(e){t.audiopath=e},expression:"audiopath"}})],1),t._v(" "),a("FormItem",{attrs:{label:"音频文件"}},[t.isShow?a("div",{staticClass:"h5ImgBox"},[a("Icon",{attrs:{type:"ios-cloud-upload",size:"40"}})],1):t._e(),t._v(" "),a("div",[a("label",{staticClass:"button",attrs:{for:"inputFile3"}},[a("span",{staticClass:"upload__select"},[t._v("点击上传音频")]),t._v(" "),t.ishowFile?a("input",{staticStyle:{display:"none"},attrs:{type:"file",id:"inputFile3",accept:"mp3"},on:{change:t.onUpload3}}):t._e()])])])],1)],1),t._v(" "),a("div",{staticClass:"zhijian-btn-box"},[a("div",{staticClass:"zhijian-btn-confirm",on:{click:function(e){t.submitForm1("formValidate1")}}},[t._v("确定")])])]),t._v(" "),a("Modal",{attrs:{title:"Common Modal dialog box title","class-name":"ma-edit-modal"},model:{value:t.moveModal,callback:function(e){t.moveModal=e},expression:"moveModal"}},[a("div",{staticClass:"edit-modal-body"},[a("div",{staticClass:"title",staticStyle:{"font-size":"24px",color:"var(--base)","text-align":"center"}},[t._v("移动")]),t._v(" "),a("RadioGroup",{staticStyle:{margin:"20px 80px"},model:{value:t.animal,callback:function(e){t.animal=e},expression:"animal"}},[a("Radio",{attrs:{label:"1"}},[t._v("上移")]),t._v(" "),a("Radio",{attrs:{label:"2"}},[t._v("下移")]),t._v(" "),a("Radio",{attrs:{label:"3"}},[t._v("移至顶部")]),t._v(" "),a("Radio",{attrs:{label:"4"}},[t._v("移至底部")])],1)],1),t._v(" "),a("div",{staticClass:"zhijian-btn-box"},[a("div",{staticClass:"zhijian-btn-confirm",on:{click:t.moveOk}},[t._v("确定")])])]),t._v(" "),a("Modal",{attrs:{title:"Common Modal dialog box title"},model:{value:t.delemodal,callback:function(e){t.delemodal=e},expression:"delemodal"}},[a("p",{staticClass:"modelp"},[t._v("请确认是否删除改课程")]),t._v(" "),a("div",{staticClass:"zhijian-btn-box"},[a("div",{staticClass:"zhijian-btn-confirm",on:{click:t.deleteOk}},[t._v("确定")])])])],1)},staticRenderFns:[]};var s=a("VU/8")(i,o,!1,function(t){a("h47t")},null,null);e.default=s.exports},h47t:function(t,e){}});