<template>
  <div id="spreadDetail">
    <div class="h1">渠道数据详情</div>
    <div class="OrderDetail_back">
      <Button @click="toList">返回</Button>
      <div class="date">
        <DatePicker
          v-model="startDate"
          type="datetime"
          placeholder="开始日期"
          style="width: 220px;"
          @on-change="getStart"
        ></DatePicker>至
        <DatePicker
          type="datetime"
          v-model="endDate"
          placeholder="结束日期"
          style="width:220px;"
          @on-change="getEnd"
        ></DatePicker>
        <Button type="primary" @click="search">搜索</Button>
      </div>
    </div>
    <div class="OrderDetail_status" v-if="table.data[0]">
      当前渠道名称：
      <span>{{table.data[0].spread_name}}</span>
    </div>
    <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>

    <Modal class="OrderDetail_detail" v-model="isShowData">
      <!-- <h2 style="margin-bottom: 16px;">{{startDate}}至{{endDate}}:</h2>
      <h2 style="margin-bottom: 16px;">{{searchCount}}</h2>-->
      <div
        class="OrderDetail_info"
        style="margin-bottom: 16px; font-size:18px"
        v-if="table.data[0]"
      >
        <label>渠道名称：</label>
        <span>{{table.data[0].spread_name}}</span>
      </div>
      <div class="OrderDetail_info" style="margin-bottom: 16px;font-size:18px">
        <label>时间间隔：</label>
        <span>{{startDate}}至{{endDate}}</span>
      </div>
      <div class="OrderDetail_info" style="margin-bottom: 16px;font-size:18px">
        <label>授权用户：</label>
        <span>{{authNum}}</span>
      </div>
      <div class="OrderDetail_info" style="font-size:18px">
        <label>首次访问用户：</label>
        <span>{{notAuthNum}}</span>
      </div>
    </Modal>
  </div>
</template>
<script>
export default {
  name: "spreadDetail",
  data() {
    return {
      startDate: "",
      endDate: "",
      isShowData: false,
      authNum: "",
      notAuthNum: "",
      table: {
        columns: [
          {
            title: "数据类别",
            align: "center",
            render: (h, params) => {
              return h(
                "div",
                params.row.is_auth === 1? "授权用户": params.row.is_auth === -1? "首次访问用户":  params.row.is_auth === 0?'新增UA用户':''
              );
            }
          },
          {
            title: "今天",
            key: "today_num",
            align: "center"
          },
          {
            title: "昨天",
            key: "yesterday_num",
            align: "center"
          },
          {
            title: "最近7天",
            key: "seven_day_num",
            align: "center"
          },
          {
            title: "最近30天",
            key: "thirty_day_num",
            align: "center"
          }
        ],
        data: []
      }
    };
  },
  created() {
    this.getDetaildata();
  },
  methods: {
    //获取列表数据(默认当日数据)
    getDetaildata() {
      this.$http
        .post(this.PATH.SPREADDATADETAIL, {
          spread_id: this.$route.query.id
        })
        .then(success => {
          console.log(success.data, "详情");
          if (success.status == 200) {
            if (success.data.errno == 0) {
              this.table.data = success.data.data;
              // let dataArr = success.data;

              // dataArr.map((item, index) => {
              //   return;
              // });
            } else {
              this.$Modal.error({
                width: 360,
                content: success.data.errmsg
              });
            }
          } else {
            this.$Message.error("Fail!");
          }
        });
    },
    //获取选择的开始时间
    getStart(value) {
      this.startDate = value;
    },
    //获取结束时间
    getEnd(value) {
      this.endDate = value;
    },
    search() {
      if (this.startDate == "" || this.endDate == "") {
        this.$Modal.error({
          width: 360,
          content: "请选择日期"
        });
        return;
      }
      this.$http
        .post(this.PATH.SPREADDATAQUERYBYDATE, {
          spread_id: this.$route.query.id,
          start_time: this.startDate,
          end_time: this.endDate
        })
        .then(res => {
          // console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.isShowData = true;
              this.authNum = res.data.data.auth_num;
              this.notAuthNum = res.data.data.not_auth_num;
            }
          }
        });
    },
    toList() {
      this.$router.push({
        name: "dataOverview"
      });
    }
  }
};
</script>
<style lang="scss">
#spreadDetail {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .OrderDetail_back {
    margin-top: 20px;
    > button {
      font-size: 16px;
    }
    .date {
      float: right;
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
  .header {
    height: 50px;
    margin-top: 20px;
    position: relative;
    .search {
      width: 200px;
      position: absolute;
      // top: 75px;
      right: 120px;
    }
    .newbtn {
      font-size: 12px;
      line-height: 10px;
      height: 32px;
      position: absolute;
      // top: 75px;
      right: 20px;
    }
  }
  .account-table {
    margin-top: 20px;
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
}

//新增编辑弹框
.ivu-radio-inner:after {
  position: absolute;
  width: 8px;
  height: 8px;
  left: 2px;
  top: 2px;
  border-radius: 6px;
  display: table;
  border-top: 0;
  border-left: 0;
  content: " ";
  background-color: #ffc639 !important;
  opacity: 0;
  transition: all 0.2s ease-in-out;
  transform: scale(0);
}
.ma-edit-modal {
  .edit-modal-body {
    position: relative;
    margin-bottom: 30px;
    font-size: 14px;
  }
  .ivu-icon-android-close {
    position: absolute;
    top: -20px;
    right: -14px;
    font-size: 24px;
    color: var(--base);
    cursor: pointer;
  }
  .title {
    margin-bottom: 24px;
    text-align: center;
    font-size: 24px;
    color: var(--base);
  }
  .ivu-radio-checked .ivu-radio-inner {
    border-color: var(--base) !important;
  }

  //弹框表单
  .edit-form {
    .error-tip {
      position: absolute;
      top: 100%;
      left: 0;
      line-height: 1;
      padding-top: 6px;
      color: #ed4958;
    }
    .role-select {
      height: 42px;
      line-height: 42px;
    }
    .department-select {
      margin-right: 12px;
    }
    .department-select,
    .job-select {
      width: 48%;
    }
  }
  .demo-spin-col {
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -60%);
  }
}
</style>
