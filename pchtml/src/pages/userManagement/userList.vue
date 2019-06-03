<template>
  <div id="userList">
    <div class="h1">用户列表</div>
    <div class="header">
      <Input
        v-model="value"
        class="search"
        search
        enter-button="搜索"
        @on-search="search"
        @on-blur="changePages"
        placeholder="请输入搜索关键字"
      />
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
      </div>
    </div>

    <Table class="zhijian-table account-table" stripe :columns="table.columns" :data="table.data"></Table>
    <div class="zhijian-pagination">
      <Page
        :total="table.total"
        :current="table.page"
        show-elevator
        @on-change="changePage"
        :pageSize="table.pagesize"
      ></Page>
    </div>
  </div>
</template>
<script>
export default {
  name: "userList",
  data() {
    return {
      value: "",
      is_search: false,
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        columns: [
          {
            title: "头像",
            key: "avatar_url",
            render: (h, params) => {
              // console.log(params);
              return h("img", {
                style: {
                  width: "35px",
                  height: "35px"
                },
                attrs: {
                  src: params.row.avatar_url
                }
              });
            }
          },
          {
            title: "昵称",
            key: "nick_name",
            align: "center"
          },
          {
            title: "性别",
            key: "gender",
            align: "center",
            render: (h, params) => {
              return h("p", params.row.gender == 1 ? "男" : "女");
            }
          },
          {
            title: "手机号",
            key: "phone",
            align: "center"
          },
          {
            title: "授权登录时间",
            key: "create_time",
            align: "center"
          }
        ],
        data: []
      },
      startDate: "", //开始时间
      endDate: "" //结束时间
    };
  },
  created() {
    this.getData();
  },
  methods: {
    getData() {
      this.$http
        .post(this.PATH.GETUSERLIST, {
          page: this.table.page,
          size: this.table.pagesize
        })
        .then(res => {
          // console.log(res);
          if (res.status == 200) {
            if (res.data.errno == 0) {
              this.table.data = res.data.list;
              this.table.total = res.data.total;
            } else {
              this.$Modal.error({
                width: 360,
                content: res.data.errmsg
              });
            }
          }
        });
    },
    changePage(page) {
      this.table.page = page;
      if (this.is_search) {
        this.search();
      } else {
        this.getData();
      }
      // this.getData();
    },
    search() {
      this.is_search = true;
      this.$http
        .post(this.PATH.USERSEARCH, {
          words: this.value,
          // is_show: this.table.is_show,
          page: this.table.page,
          pagesize: this.table.pagesize,
          start_time: this.startDate,
          end_time: this.endDate
        })
        .then(res => {
          console.log(res, "user");
          if (res.status == 200) {
            this.table.data = res.data.data;
            this.table.total = res.data.count;
          }
        });
    },
    changePages() {
      this.table.page = 1;
    },
    //获取选择的开始时间
    getStart(value) {
      this.startDate = value;
    },
    //获取结束时间
    getEnd(value) {
      this.endDate = value;
    }
  }
};
</script>
<style lang="scss" scoped>
#userList {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .ivu-picker-panel-body {
    background-color: #fff !important;
  }
  .header {
    height: 50px;
    .date {
      float: right;
    }
  }
  .h1 {
    font-size: 22px;
    color: #808080;
  }
  .account-table {
    margin-top: 20px;
  }
  .search {
    float: right;
    width: 200px;
    // position: absolute;
    // top: 80px;
    // right: 100px;
  }
}
</style>
