<template>
  <div id="OrderDetail">
    <div class="OrderDetail_back">
      <Button @click="toList">返回</Button>
    </div>
    <div class="OrderDetail_status">
      当前订单状态：
      <span
        v-if="baseInfo"
      >{{baseInfo.order_status==1?'待付款':baseInfo.order_status==2?'待发货':baseInfo.order_status==3?'待收货':baseInfo.order_status==4?'已完成':baseInfo.order_status==5?'已关闭':''}}</span>
    </div>
    <div class="OrderDetail_detail">
      <h4>基本信息：</h4>
      <div class="OrderDetail_info" v-if="baseInfo">
        <img :src="userInfo.avatar_url">
        <span>{{userInfo.nick_name}}</span>
      </div>
    </div>
    <div class="OrderDetail_detail">
      <Table :data="tableData" :columns="tableColumns" stripe></Table>
    </div>
    <div class="OrderDetail_detail">
      <h4>物流信息：</h4>
      <div class="OrderDetail_info">
        <label>收货信息：</label>
        <span
          v-if="addressInfo"
        >{{addressInfo.name}} &nbsp;&nbsp;{{addressInfo.phone}}&nbsp;&nbsp; {{(addressInfo.province?addressInfo.province:'')+(addressInfo.city?addressInfo.city:'')+(addressInfo.area?addressInfo.area:'')+(addressInfo.detail?addressInfo.detail:'')}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>运送方式：</label>
        <div v-if="expressData">
          <span v-if="expressData.express_num">快递</span>
          <span v-if="!expressData.express_num ">非快递</span>
        </div>
      </div>
      <div class="OrderDetail_info">
        <label>物流公司名称：</label>
        <span v-if="expressData">{{expressData.company}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>运单号：</label>
        <span v-if="expressData">{{expressData.express_num}}</span>
      </div>
    </div>
    <div class="OrderDetail_detail">
      <h4></h4>
      <div class="OrderDetail_info">
        <label>订单号：</label>
        <span v-if="baseInfo">{{baseInfo.order_num}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>创建时间：</label>
        <span v-if="baseInfo">{{baseInfo.create_time}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>付款时间：</label>
        <span v-if="baseInfo">{{baseInfo.pay_time}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>发货时间：</label>
        <span v-if="baseInfo">{{baseInfo.send_time}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>完成时间：</label>
        <span v-if="baseInfo">{{baseInfo.receive_time}}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "orderDetail",
  data() {
    return {
      baseInfo: null,
      addressInfo: null,
      tableData: [],
      expressData: null,
      userInfo: null,
      tableColumns: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            // console.log("params.row", params.row);
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.min_pic
                },
                style: {
                  width: "100px",
                  height: "70px",
                  border: "1px solid",
                  marginRight: "20px",
                  verticalAlign: "middle",
                  marginTop: "10px"
                }
              }),
              h(
                "p",
                {
                  style: {
                    width: "160px",
                    height: "55px",
                    marginTop: "-65px",
                    marginLeft: "120px",
                    overflow: "hidden",
                    marginBottom: "20px"
                  }
                },
                params.row.name
              )
            ]);
          }
        },
        {
          title: "状态",
          key: "order_status",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.order_status == 1
                  ? "待付款"
                  : params.row.order_status == 2
                  ? "待发货"
                  : params.row.order_status == 3
                  ? "待收货"
                  : params.row.order_status == 4
                  ? "已完成"
                  : params.row.order_status == 5
                  ? "已关闭"
                  : ""
              )
            ]);
          }
        }
        // {
        //   title: "数量",
        //   key: "goods_num",
        //   align: "center"
        // }
      ]
    };
  },
  created() {
    this.getDetail();
  },
  methods: {
    getDetail() {
      this.$http
        .post(this.PATH.PCGOODSORDERDETAIL, { order_id: +this.$route.query.id })
        .then(res => {
          if (res.data.errno === 0) {
            console.log("订单详情", res);
            res.data.data.goods_data.order_status =
              res.data.data.order_data.order_status;
            this.tableData = [res.data.data.goods_data];
            this.baseInfo = res.data.data.order_data;
            // this.tableData.order_status = this.baseInfo.order_status;
            this.addressInfo = res.data.data.address_data;
            this.expressData = res.data.data.express_data;
            this.userInfo = res.data.data.user_data;
            console.log("this.baseInfo", this.baseInfo);
          } else {
            this.$Modal.error({
              title: "提示",
              content: res.data.errmsg
            });
          }
        });
    },
    toList() {
      this.$router.push({
        name: "orderList"
      });
    }
  }
};
</script>

<style lang="scss" scoped>
#OrderDetail {
  height: 100%;
  padding: 20px 20px 65px 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
}
.OrderDetail_back {
  > button {
    font-size: 16px;
  }
}
.OrderDetail_status {
  width: 80%;
  padding: 30px;
  font-size: 20px;
  span {
    color: #ff7667;
    font-weight: bold;
  }
}
.OrderDetail_detail {
  margin-bottom: 20px;
  h4 {
    font-size: 18px;
    padding-bottom: 15px;
    border-bottom: 1px solid #000;
  }
}
.OrderDetail_info {
  margin-top: 20px;
  &:after {
    content: "";
    display: block;
    clear: both;
  }
  img {
    float: left;
    width: 60px;
    height: 60px;
  }
  > label {
    width: 120px;
    height: 60px;
    line-height: 60px;
    float: left;
  }
  span {
    margin-left: 10px;
    float: left;
    display: inline-block;
    line-height: 60px;
    font-weight: bold;
  }
}
</style>
