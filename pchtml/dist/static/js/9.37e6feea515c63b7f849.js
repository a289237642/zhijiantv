webpackJsonp([9],{CgOh:function(a,e,s){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var t={name:"orderDetail",data:function(){return{baseInfo:null,addressInfo:null,tableData:[],expressData:null,userInfo:null,tableColumns:[{title:"商品描述",key:"goods_name",width:300,render:function(a,e){return a("div",[a("img",{attrs:{src:e.row.min_pic},style:{width:"100px",height:"70px",border:"1px solid",marginRight:"20px",verticalAlign:"middle",marginTop:"10px"}}),a("p",{style:{width:"160px",height:"55px",marginTop:"-65px",marginLeft:"120px",overflow:"hidden",marginBottom:"20px"}},e.row.name)])}},{title:"状态",key:"order_status",align:"center",render:function(a,e){return a("div",[a("p",1==e.row.order_status?"待付款":2==e.row.order_status?"待发货":3==e.row.order_status?"待收货":4==e.row.order_status?"已完成":5==e.row.order_status?"已关闭":"")])}}]}},created:function(){this.getDetail()},methods:{getDetail:function(){var a=this;this.$http.post(this.PATH.PCGOODSORDERDETAIL,{order_id:+this.$route.query.id}).then(function(e){0===e.data.errno?(e.data.data.goods_data.order_status=e.data.data.order_data.order_status,a.tableData=[e.data.data.goods_data],a.baseInfo=e.data.data.order_data,a.addressInfo=e.data.data.address_data,a.expressData=e.data.data.express_data,a.userInfo=e.data.data.user_data):a.$Modal.error({title:"提示",content:e.data.errmsg})})},toList:function(){this.$router.push({name:"orderList"})}}},r={render:function(){var a=this,e=a.$createElement,s=a._self._c||e;return s("div",{attrs:{id:"OrderDetail"}},[s("div",{staticClass:"OrderDetail_back"},[s("Button",{on:{click:a.toList}},[a._v("返回")])],1),a._v(" "),s("div",{staticClass:"OrderDetail_status"},[a._v("\n    当前订单状态：\n    "),a.baseInfo?s("span",[a._v(a._s(1==a.baseInfo.order_status?"待付款":2==a.baseInfo.order_status?"待发货":3==a.baseInfo.order_status?"待收货":4==a.baseInfo.order_status?"已完成":5==a.baseInfo.order_status?"已关闭":""))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_detail"},[s("h4",[a._v("基本信息：")]),a._v(" "),a.baseInfo?s("div",{staticClass:"OrderDetail_info"},[s("img",{attrs:{src:a.userInfo.avatar_url}}),a._v(" "),s("span",[a._v(a._s(a.userInfo.nick_name))])]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_detail"},[s("Table",{attrs:{data:a.tableData,columns:a.tableColumns,stripe:""}})],1),a._v(" "),s("div",{staticClass:"OrderDetail_detail"},[s("h4",[a._v("物流信息：")]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("收货信息：")]),a._v(" "),a.addressInfo?s("span",[a._v(a._s(a.addressInfo.name)+"   "+a._s(a.addressInfo.phone)+"   "+a._s((a.addressInfo.province?a.addressInfo.province:"")+(a.addressInfo.city?a.addressInfo.city:"")+(a.addressInfo.area?a.addressInfo.area:"")+(a.addressInfo.detail?a.addressInfo.detail:"")))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("运送方式：")]),a._v(" "),a.expressData?s("div",[a.expressData.express_num?s("span",[a._v("快递")]):a._e(),a._v(" "),a.expressData.express_num?a._e():s("span",[a._v("非快递")])]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("物流公司名称：")]),a._v(" "),a.expressData?s("span",[a._v(a._s(a.expressData.company))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("运单号：")]),a._v(" "),a.expressData?s("span",[a._v(a._s(a.expressData.express_num))]):a._e()])]),a._v(" "),s("div",{staticClass:"OrderDetail_detail"},[s("h4"),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("订单号：")]),a._v(" "),a.baseInfo?s("span",[a._v(a._s(a.baseInfo.order_num))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("创建时间：")]),a._v(" "),a.baseInfo?s("span",[a._v(a._s(a.baseInfo.create_time))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("付款时间：")]),a._v(" "),a.baseInfo?s("span",[a._v(a._s(a.baseInfo.pay_time))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("发货时间：")]),a._v(" "),a.baseInfo?s("span",[a._v(a._s(a.baseInfo.send_time))]):a._e()]),a._v(" "),s("div",{staticClass:"OrderDetail_info"},[s("label",[a._v("完成时间：")]),a._v(" "),a.baseInfo?s("span",[a._v(a._s(a.baseInfo.receive_time))]):a._e()])])])},staticRenderFns:[]};var d=s("VU/8")(t,r,!1,function(a){s("G/9S")},"data-v-da804872",null);e.default=d.exports},"G/9S":function(a,e){}});