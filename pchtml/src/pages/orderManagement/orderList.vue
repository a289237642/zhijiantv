<template>
  <div id="OrderList">
    <div class="h1">订单列表</div>
    <!-- <div class="orderListSearch">
      <div>
        <div>
          <label>商品名称</label>
          <Input v-model="commodity" placeholder="请输入商品名称" style="width: 300px"/>
        </div>
        <div>
          <label>订单编号</label>
          <Input v-model="OrderNum" placeholder="请输入订单编号" style="width: 300px"/>
        </div>
        <div>
          <label>收货人姓名</label>
          <Input v-model="consignee" placeholder="请输入收货人姓名" style="width: 300px"/>
        </div>
      </div>
      <div>
        <div>
          <label>下单时间</label>
          <DatePicker
            type="datetimerange"
            placeholder="请选择下单时间"
            style="width: 300px"
            @on-change="changeOrderTime"
            v-model="fakeOrderTime"
          ></DatePicker>
        </div>
        <div>
          <label>订货状态</label>
          <Select v-model="orderStatus" style="width:300px">
            <Option
              v-for="(item,index) in orderStatusList"
              :value="item.status"
              :key="index"
            >{{ item.value }}</Option>
          </Select>
        </div>
        <div>
          <label>收货人手机号</label>
          <Input v-model="phoneNum" placeholder="请输入收货人手机号" style="width: 300px"/>
        </div>
      </div>
      <section>
        <Button type="error" @click="searchOrder(1)">筛选订单</Button>
        <Button @click="clearSearch">清空筛选条件</Button>
      </section>
    </div>-->
    <div class="orderListTable">
      <Tabs value="6" @on-click="changeOrderTabs">
        <TabPane label="全部" name="6">
          <Table :data="allData6" :columns="allColumns6" stripe></Table>
          <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
              <Page :total="total6" :current="1" @on-change="changePage6"></Page>
            </div>
          </div>
        </TabPane>
        <!-- <TabPane label="进行中" name="1">
            <Table :data="allData5" :columns="allColumns5" stripe ></Table>
            <div style="margin: 10px;overflow: hidden">
              <div style="float: right;">
                <Page :total="total5" :current="1" @on-change="changePage5"></Page>
              </div>
            </div>
        </TabPane>-->
        <TabPane label="待发货" name="2">
          <Table :data="allData2" :columns="allColumns2" stripe></Table>
          <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
              <Page :total="total2" :current="1" @on-change="changePage2"></Page>
            </div>
          </div>
        </TabPane>
        <TabPane label="已发货" name="3">
          <Table :data="allData3" :columns="allColumns3" stripe></Table>
          <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
              <Page :total="total3" :current="1" @on-change="changePage3"></Page>
            </div>
          </div>
        </TabPane>
        <TabPane label="已完成" name="4">
          <Table :data="allData4" :columns="allColumns4" stripe></Table>
          <div style="margin: 10px;overflow: hidden">
            <div style="float: right;">
              <Page :total="total4" :current="1" @on-change="changePage4"></Page>
            </div>
          </div>
        </TabPane>
      </Tabs>
    </div>
    <Modal v-model="modalSend">
      <h3>请输入物流信息</h3>
      <div class="orderListModal">
        <div>
          <label>运送方式：</label>
          <RadioGroup v-model="way">
            <Radio label="1">
              <span>快递</span>
            </Radio>
            <Radio label="0">
              <span>无需快递</span>
            </Radio>
          </RadioGroup>
        </div>
        <div v-if="way==1">
          <label>物流公司名称：</label>
          <Input style="width: 200px" v-model="company"/>
          <!-- <Select v-model="modelSelect" style="width:200px">
            <Option
              v-for="(item,index) in logisticList"
              :value="item.express_id"
              :key="index"
            >{{ item.name }}</Option>
          </Select>-->
        </div>
        <div v-if="way==1">
          <label>运单号：</label>
          <Input style="width: 200px" v-model="modelNote"/>
        </div>
        <div>
          <label>备注：</label>
          <Input type="textarea" style="width: 200px" v-model="textarea"/>
        </div>
      </div>
      <div class="orderListBtn">
        <Button @click="modalCancel">取消</Button>
        <Button @click="modalSendConfirm">确定</Button>
      </div>
    </Modal>
    <Modal v-model="modalClose">
      <h3>请确认是否关闭订单</h3>
      <!-- <div class="orderListModal">
        <div>
          <label>备注：</label>
          <Input
            type="textarea"
            v-model="modalRemark"
            :autosize="{maxRows: 3,minRows: 3}"
            style="width: 200px"
          />
        </div>
      </div>-->
      <div class="orderListBtn">
        <Button @click="modalCancel">取消</Button>
        <Button @click="modalCloseConfirm">确定</Button>
      </div>
    </Modal>
    <Modal class="OrderDetail_detail" v-model="isShowlogistics">
      <h3 style="margin-bottom: 16px;">物流信息：</h3>
      <div class="OrderDetail_info">
        <label>运送方式：</label>
        <div v-if="logisticsInfo">
          <span v-if="logisticsInfo.express_num">快递</span>
          <span v-if="!logisticsInfo.express_num ">非快递</span>
        </div>
      </div>
      <div class="OrderDetail_info">
        <label>物流公司名称：</label>
        <span v-if="logisticsInfo">{{logisticsInfo.company}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>运单号：</label>
        <span v-if="logisticsInfo">{{logisticsInfo.express_num}}</span>
      </div>
      <div class="OrderDetail_info">
        <label>备注信息：</label>
        <span v-if="logisticsInfo">{{logisticsInfo.remark}}</span>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  name: "orderList",
  data() {
    return {
      commodity: "",
      OrderNum: "",
      consignee: "",
      orderTime: "",
      fakeOrderTime: "",
      orderStatus: 6,
      phoneNum: "",
      modalSend: false,
      modalClose: false,
      modelSelect: "",
      modelNote: "",
      textarea: "",
      way: "1",
      logisticList: [],
      orderId: "",
      modalRemark: "",
      tabName: 6,
      orderStatusList: [
        // {status: 1,value: '进行中'},
        { status: 2, value: "待发货" },
        { status: 3, value: "已发货" },
        { status: 4, value: "已完成" },
        { status: 5, value: "已关闭" }
      ],
      allColumns1: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.img_url
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
                params.row.goods_name
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
        },
        {
          title: "姓名",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.name
                  : ""
              )
            ]);
          }
        },
        {
          title: "手机号码",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.phone
                  : ""
              )
            ]);
          }
        },
        {
          title: "地址",

          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? (params.row.address_data.provence
                      ? params.row.address_data.provence
                      : "") +
                      (params.row.address_data.city
                        ? params.row.address_data.city
                        : "") +
                      (params.row.address_data.area
                        ? params.row.address_data.area
                        : "") +
                      (params.row.address_data.detail
                        ? params.row.address_data.detail
                        : "")
                  : "无"
              )
            ]);
          }
        },
        {
          title: "订单号",
          key: "order_num",
          align: "center"
        },
        {
          title: "兑换时间",
          key: "create_time",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.create_time === "None"
                  ? "无"
                  : params.row.create_time
              )
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            let isOn = "发货";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.order_status > 2) {
              isOn = "物流信息";
            } else if (params.row.order_status == 2) {
              isOn = "发货";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display:
                      params.row.order_status == 5 ||
                      params.row.order_status == 1
                        ? "none"
                        : "inline"
                  },
                  on: {
                    click: () => {
                      if (isOn === "发货") {
                        this.modalSend = true;
                        this.orderId = params.row.id;
                      } else {
                        this.showlogistics(params.row.id);
                      }
                    }
                  }
                },
                isOn
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display: params.row.order_status == 5 ? "inline" : "none"
                  },
                  on: {
                    click: () => {
                      this.modalClose = true;
                      this.orderId = params.row.id;
                    }
                  }
                },
                Number(params.row.order_status) === 5 ? "已关闭" : "关闭"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.toDetail(params.row.id);
                    }
                  }
                },
                "详情"
              )
            ]);
          }
        }
      ],
      allColumns5: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.img_url
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
                params.row.goods_name
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
        },
        {
          title: "姓名",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.name
                  : ""
              )
            ]);
          }
        },
        {
          title: "手机号码",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.phone
                  : ""
              )
            ]);
          }
        },
        {
          title: "地址",

          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? (params.row.address_data.provence
                      ? params.row.address_data.provence
                      : "") +
                      (params.row.address_data.city
                        ? params.row.address_data.city
                        : "") +
                      (params.row.address_data.area
                        ? params.row.address_data.area
                        : "") +
                      (params.row.address_data.detail
                        ? params.row.address_data.detail
                        : "")
                  : "无"
              )
            ]);
          }
        },
        {
          title: "订单号",
          key: "order_num",
          align: "center"
        },
        {
          title: "兑换时间",
          key: "create_time",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.create_time === "None"
                  ? "无"
                  : params.row.create_time
              )
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            let isOn = "发货";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.order_status > 2) {
              isOn = "物流信息";
            } else if (params.row.order_status == 2) {
              isOn = "发货";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display:
                      params.row.order_status == 5 ||
                      params.row.order_status == 1
                        ? "none"
                        : "inline"
                  },
                  on: {
                    click: () => {
                      if (isOn === "发货") {
                        this.modalSend = true;
                        this.orderId = params.row.id;
                      } else {
                        this.showlogistics(params.row.id);
                      }
                    }
                  }
                },
                isOn
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display: params.row.order_status == 5 ? "inline" : "none"
                  },
                  on: {
                    click: () => {
                      this.modalClose = true;
                      this.orderId = params.row.id;
                    }
                  }
                },
                Number(params.row.order_status) === 5 ? "已关闭" : "关闭"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.toDetail(params.row.id);
                    }
                  }
                },
                "详情"
              )
            ]);
          }
        }
      ],
      allColumns2: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.img_url
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
                params.row.goods_name
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
        },
        {
          title: "姓名",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.name
                  : ""
              )
            ]);
          }
        },
        {
          title: "手机号码",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.phone
                  : ""
              )
            ]);
          }
        },
        {
          title: "地址",

          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? (params.row.address_data.provence
                      ? params.row.address_data.provence
                      : "") +
                      (params.row.address_data.city
                        ? params.row.address_data.city
                        : "") +
                      (params.row.address_data.area
                        ? params.row.address_data.area
                        : "") +
                      (params.row.address_data.detail
                        ? params.row.address_data.detail
                        : "")
                  : "无"
              )
            ]);
          }
        },
        {
          title: "订单号",
          key: "order_num",
          align: "center"
        },
        {
          title: "兑换时间",
          key: "create_time",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.create_time === "None"
                  ? "无"
                  : params.row.create_time
              )
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            let isOn = "发货";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.order_status > 2) {
              isOn = "物流信息";
            } else if (params.row.order_status == 2) {
              isOn = "发货";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display:
                      params.row.order_status == 5 ||
                      params.row.order_status == 1
                        ? "none"
                        : "inline"
                  },
                  on: {
                    click: () => {
                      if (isOn === "发货") {
                        this.modalSend = true;
                        this.orderId = params.row.id;
                      } else {
                        this.showlogistics(params.row.id);
                      }
                    }
                  }
                },
                isOn
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display: params.row.order_status == 5 ? "inline" : "none"
                  },
                  on: {
                    click: () => {
                      this.modalClose = true;
                      this.orderId = params.row.id;
                    }
                  }
                },
                Number(params.row.order_status) === 5 ? "已关闭" : "关闭"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.toDetail(params.row.id);
                    }
                  }
                },
                "详情"
              )
            ]);
          }
        }
      ],
      allColumns3: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.img_url
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
                params.row.goods_name
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
        },
        {
          title: "姓名",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.name
                  : ""
              )
            ]);
          }
        },
        {
          title: "手机号码",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.phone
                  : ""
              )
            ]);
          }
        },
        {
          title: "地址",

          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? (params.row.address_data.provence
                      ? params.row.address_data.provence
                      : "") +
                      (params.row.address_data.city
                        ? params.row.address_data.city
                        : "") +
                      (params.row.address_data.area
                        ? params.row.address_data.area
                        : "") +
                      (params.row.address_data.detail
                        ? params.row.address_data.detail
                        : "")
                  : "无"
              )
            ]);
          }
        },

        {
          title: "订单号",
          key: "order_num",
          align: "center"
        },
        {
          title: "兑换时间",
          key: "create_time",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.create_time === "None"
                  ? "无"
                  : params.row.create_time
              )
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            let isOn = "发货";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.order_status > 2) {
              isOn = "物流信息";
            } else if (params.row.order_status == 2) {
              isOn = "发货";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display:
                      params.row.order_status == 5 ||
                      params.row.order_status == 1
                        ? "none"
                        : "inline"
                  },
                  on: {
                    click: () => {
                      if (isOn === "发货") {
                        this.modalSend = true;
                        this.orderId = params.row.id;
                      } else {
                        this.showlogistics(params.row.id);
                      }
                    }
                  }
                },
                isOn
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display: params.row.order_status == 5 ? "inline" : "none"
                  },
                  on: {
                    click: () => {
                      this.modalClose = true;
                      this.orderId = params.row.id;
                    }
                  }
                },
                Number(params.row.order_status) === 5 ? "已关闭" : "关闭"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.toDetail(params.row.id);
                    }
                  }
                },
                "详情"
              )
            ]);
          }
        }
      ],
      allColumns4: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.img_url
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
                params.row.goods_name
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
        },
        {
          title: "姓名",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.name
                  : ""
              )
            ]);
          }
        },
        {
          title: "手机号码",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.phone
                  : ""
              )
            ]);
          }
        },
        {
          title: "地址",

          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? (params.row.address_data.provence
                      ? params.row.address_data.provence
                      : "") +
                      (params.row.address_data.city
                        ? params.row.address_data.city
                        : "") +
                      (params.row.address_data.area
                        ? params.row.address_data.area
                        : "") +
                      (params.row.address_data.detail
                        ? params.row.address_data.detail
                        : "")
                  : "无"
              )
            ]);
          }
        },
        {
          title: "订单号",
          key: "order_num",
          align: "center"
        },
        {
          title: "兑换时间",
          key: "create_time",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.create_time === "None"
                  ? "无"
                  : params.row.create_time
              )
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            let isOn = "发货";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.order_status > 2) {
              isOn = "物流信息";
            } else if (params.row.order_status == 2) {
              isOn = "发货";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display:
                      params.row.order_status == 5 ||
                      params.row.order_status == 1
                        ? "none"
                        : "inline"
                  },
                  on: {
                    click: () => {
                      if (isOn === "发货") {
                        this.modalSend = true;
                        this.orderId = params.row.id;
                      } else {
                        this.showlogistics(params.row.id);
                      }
                    }
                  }
                },
                isOn
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display: params.row.order_status == 5 ? "inline" : "none"
                  },
                  on: {
                    click: () => {
                      this.modalClose = true;
                      this.orderId = params.row.id;
                    }
                  }
                },
                Number(params.row.order_status) === 5 ? "已关闭" : "关闭"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.toDetail(params.row.id);
                    }
                  }
                },
                "详情"
              )
            ]);
          }
        }
      ],
      allColumns6: [
        {
          title: "商品描述",
          key: "goods_name",
          width: 300,
          render: (h, params) => {
            return h("div", [
              h("img", {
                attrs: {
                  src: params.row.img_url
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
                params.row.goods_name
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
        },
        {
          title: "姓名",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",

                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.name
                  : ""
              )
            ]);
          }
        },
        {
          title: "手机号码",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.hasOwnProperty("address_data")
                  ? params.row.address_data.phone
                  : ""
              )
            ]);
          }
        },
        {
          title: "地址",
          key: "address_data",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",

                params.row.hasOwnProperty("address_data")
                  ? (params.row.address_data.provence
                      ? params.row.address_data.provence
                      : "") +
                      (params.row.address_data.city
                        ? params.row.address_data.city
                        : "") +
                      (params.row.address_data.area
                        ? params.row.address_data.area
                        : "") +
                      (params.row.address_data.detail
                        ? params.row.address_data.detail
                        : "")
                  : "无"
              )
            ]);
          }
        },
        {
          title: "订单号",
          key: "order_num",
          align: "center"
        },
        {
          title: "兑换时间",
          key: "create_time",
          align: "center",
          render: (h, params) => {
            return h("div", [
              h(
                "p",
                params.row.create_time === "None"
                  ? "无"
                  : params.row.create_time
              )
            ]);
          }
        },
        {
          title: "操作",
          key: "action",
          width: 150,
          align: "center",
          render: (h, params) => {
            let isOn = "发货";
            let bgColor = "#FFC639";
            let color = "#fff";
            if (params.row.order_status > 2) {
              isOn = "物流信息";
            } else if (params.row.order_status == 2) {
              isOn = "发货";
            }
            return h("div", [
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display:
                      params.row.order_status == 5 ||
                      params.row.order_status == 1
                        ? "none"
                        : "inline"
                  },
                  on: {
                    click: () => {
                      if (isOn === "发货") {
                        this.modalSend = true;
                        this.orderId = params.row.id;
                      } else {
                        this.showlogistics(params.row.id);
                      }
                    }
                  }
                },
                isOn
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small",
                    disabled:
                      Number(params.row.order_status) === 5 ? true : false
                  },
                  style: {
                    marginRight: "5px",
                    display: params.row.order_status == 5 ? "inline" : "none"
                  },
                  on: {
                    click: () => {
                      this.modalClose = true;
                      this.orderId = params.row.id;
                    }
                  }
                },
                Number(params.row.order_status) === 5 ? "已关闭" : "关闭"
              ),
              h(
                "Button",
                {
                  props: {
                    type: "primary",
                    size: "small"
                  },
                  style: {
                    marginRight: "5px"
                  },
                  on: {
                    click: () => {
                      this.toDetail(params.row.id);
                    }
                  }
                },
                "详情"
              )
            ]);
          }
        }
      ],
      allData1: [],
      allData2: [],
      allData3: [],
      allData4: [],
      allData5: [],
      allData6: [],
      total1: 0,
      total2: 0,
      total3: 0,
      total4: 0,
      total5: 0,
      total6: 0,
      page1: 1, // 待付款
      page2: 1, // 待发货
      page3: 1, // 待收货
      page4: 1, // 已完成
      page5: 1, // 已取消
      page6: 1, // 全部
      pagesize1: 10, // 待付款
      pagesize2: 10, // 待发货
      pagesize3: 10, // 待收货
      pagesize4: 10, // 已完成
      pagesize5: 10, // 已取消
      pagesize6: 10, // 全部
      company: "",
      isShowlogistics: false,
      logisticsInfo: null
    };
  },
  created() {
    //1,进行中,2,dai发货,3,已发货,4,已完成,5,已放弃,6,已关闭
    // 123456对应待付款 待发货 待收货 已完成 已取消 全部
    this.getList(6);
    this.getLogistic();
  },
  methods: {
    searchOrder(page) {
      let data = new Object();
      data.goods_name = this.commodity;
      data.receive_name = this.consignee;
      data.receive_phone = this.phoneNum;
      data.order_num = this.OrderNum;
      data.order_status = this.orderStatus;
      data.page = page;
      data.order_create_start_time = this.orderTime[0];
      data.order_create_end_time = this.orderTime[1];
      this.$http.post(this.PATH.SEARCH_ORDER, data).then(res => {
        console.log(res);
        if (res.data.errno === 0) {
          this.total1 = res.data.count;
          this.allData1 = res.data.order_list;
        } else {
          this.$Modal.error({
            title: "提示",
            content: res.data.errmsg
          });
        }
      });
    },
    getList(index) {
      console.log("index", index);
      let data = new Object();
      // data.status = index;
      data.order_status = index;

      if (index == 1) {
        data.page = this.page1;
        data.pagesize = this.pagesize1;
      } else if (index == 2) {
        data.page = this.page2;
        data.pagesize = this.pagesize2;
      } else if (index == 3) {
        data.page = this.page3;
        data.pagesize = this.pagesize3;
      } else if (index == 4) {
        data.page = this.page4;
        data.pagesize = this.pagesize4;
      } else if (index == 5) {
        data.page = this.page5;
        data.pagesize = this.pagesize5;
      } else if (index == 6) {
        data.page = this.page6;
        data.pagesize = this.pagesize6;
      }
      console.log("data", data);
      this.$http.post(this.PATH.PCGOODSORDERLS, data).then(res => {
        console.log("订单列表", res);
        if (res.data.errno === 0) {
          if (index === 1) {
            this.total1 = res.data.data.count;
            this.allData1 = res.data.data.order_list;
          } else if (index === 2) {
            this.total2 = res.data.data.count;
            this.allData2 = res.data.data.order_list;
          } else if (index === 3) {
            this.total3 = res.data.data.count;
            this.allData3 = res.data.data.order_list;
          } else if (index === 4) {
            this.total4 = res.data.data.count;
            this.allData4 = res.data.data.order_list;
          } else if (index === 5) {
            this.total5 = res.data.data.count;
            this.allData5 = res.data.data.order_list;
          } else if (index === 6) {
            this.total6 = res.data.data.count;
            this.allData6 = res.data.data.order_list;
          }
        } else {
          this.$Modal.error({
            title: "提示",
            content: res.data.errmsg
          });
        }
      });
    },
    getLogistic() {
      this.$http.post(this.PATH.GET_EXPRESS, {}).then(res => {
        console.log(res);
        if (res.data.errno === 0) {
          this.logisticList = res.data.data;
        } else {
          this.$Modal.error({
            title: "提示",
            content: res.data.errmsg
          });
        }
      });
    },
    changeOrderTabs(val) {
      console.log("tab", val);
      this.tabName = val;
      if (this.orderStatus !== 6 && Number(val) === 6) {
        this.searchOrder();
      } else {
        this.getList(Number(val));
      }
    },
    modalSendConfirm() {
      let data = new Object();
      if (this.way == 1) {
        // data.way = "快递";
        data.order_id = this.orderId;
        data.company = this.company;
        // data.express_id = this.modelSelect;
        data.express_num = this.modelNote;
        data.remark = this.textarea;
      } else {
        // data.way = "无需快递";
        data.order_id = this.orderId;
        data.remark = this.textarea;
      }
      console.log("发货参数", data);
      this.$http.post(this.PATH.BULKSENDGOODS, data).then(res => {
        console.log("发货结果", res);
        if (res.data.errno === 0) {
          this.$Message.success("操作成功");
          this.modalCancel();
          this.getList(Number(this.tabName));
        } else {
          this.$Message.error(res.data.errmsg);
        }
      });
    },
    modalCloseConfirm() {
      let data = new Object();
      // data.remark = this.modalRemark;
      data.order_id = this.orderId;
      this.$http.post(this.PATH.PCGOODSORDERCLOSE, data).then(res => {
        console.log(res);
        if (res.data.errno === 0) {
          this.$Message.success("操作成功");
          this.modalCancel();
          this.getList(Number(this.tabName));
        } else {
          this.$Message.error(res.data.errmsg);
        }
      });
    },
    showlogistics(order_id) {
      console.log("order_id", order_id);
      this.$http
        .post(this.PATH.PCEXPRESSINFO, {
          order_id
        })
        .then(res => {
          console.log("wuliu", res);
          if (res.data.errno == 0) {
            this.logisticsInfo = res.data.data;
            this.isShowlogistics = true;
          } else {
            this.$Message.error(res.data.errmsg);
          }
        });
    },
    modalCancel() {
      this.modalSend = false;
      this.modalClose = false;
      this.orderId = "";
      this.modalRemark = "";
      this.modelSelect = "";
      this.modelNote = "";
    },
    toDetail(id) {
      this.$router.push({
        name: "orderDetail",
        query: {
          id: id
        }
      });
    },
    changePage6(page) {
      this.page6 = page;
      console.log("this.orderStatus", this.orderStatus);
      if (this.orderStatus === 6) {
        this.getList(6);
      } else {
        this.searchOrder(page);
      }
    },
    changePage2(page) {
      this.page2 = page;
      this.getList(2);
    },
    changePage3(page) {
      this.page3 = page;
      this.getList(3);
    },
    changePage4(page) {
      this.page4 = page;
      this.getList(4);
    },
    changePage5(page) {
      this.page5 = page;
      this.getList(5);
    },
    // changePage6(page) {
    //   this.page6 = page;
    //   this.getList(6);
    // },
    changeOrderTime(val) {
      console.log(val);
      this.orderTime = val;
    },
    clearSearch() {
      this.commodity = this.OrderNum = "";
      this.consignee = "";
      this.orderTime = "";
      this.fakeOrderTime = "";
      this.orderStatus = 6;
      this.phoneNum = "";
    }
  }
};
</script>
<style lang="scss" scoped>
#OrderList {
  height: 100%;
  padding: 20px 20px 65px 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  overflow: auto;
  .h1 {
    font-size: 22px;
    color: #808080;
  }
}
.orderListSearch {
  margin: 0 auto;
  &:after {
    content: "";
    clear: both;
    display: block;
  }
  width: 80%;
  > section {
    clear: both;
    > button {
      &:not(:last-of-type) {
        margin-right: 10px;
      }
    }
  }
  > div {
    float: left;
    &:first-of-type {
      margin-right: 50px;
    }
    &:after {
      content: "";
      display: block;
      clear: both;
    }
    > div {
      margin-bottom: 20px;
      label {
        display: inline-block;
        width: 75px;
      }
    }
  }
}
.orderListTable {
  margin-top: 30px;
}
.orderListModal {
  margin-top: 20px;
  > div {
    text-align: center;
    margin-bottom: 20px;
    label {
      display: inline-block;
      width: 120px;
    }
  }
}
.orderListBtn {
  text-align: center;
  > button {
    &:first-of-type {
      margin-right: 20px;
    }
    &:last-of-type {
      background-color: #000;
      color: #fff;
    }
  }
}
.OrderDetail_info {
  margin-bottom: 10px;
  span {
    margin-left: 10px;
    float: left;
    display: inline-block;
    line-height: 60px;
    font-weight: bold;
  }
}
.OrderDetail_info {
  margin-top: 10px;
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
