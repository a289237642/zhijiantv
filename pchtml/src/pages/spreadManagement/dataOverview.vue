<template>
  <div id="dataOverview">
    <div class="h1">数据概览</div>
    <div class="header">
      <Input
        search
        enter-button="搜索"
        placeholder="快速搜索"
        class="search"
        @on-search="getSearch"
        @on-blur="table.page = 1"
        @on-enter="table.page = 1"
        v-model="searchValue"
      />
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
  name: "dataOverview",
  data() {
    return {
      isShow: false, // 显示图片
      editModal: false, // 新增编辑弹框
      is_search: false,
      searchValue: "",
      table: {
        page: 1,
        pagesize: 10,
        total: 50,
        columns: [
          {
            title: "序号",
            key: "location",
            align: "center",
            width: 150
          },

          {
            title: "渠道名称",
            key: "spread_name",
            align: "center"
          },
          {
            title: "授权用户总数",
            key: "auth_num",
            align: "center"
          },
          {
            title: "首次访问用户总数",
            key: "not_auth_num",
            align: "center"
          },
          {
            title: "操作",
            align: "center",
            render: (h, params) => {
              return h("div", [
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
                        this.goToDetail(params.row);
                      }
                    }
                  },
                  "详情"
                )
              ]);
            }
          }
        ],
        data: []
      }
    };
  },
  created() {
    this.getdata(this.table.page, this.table.pagesize);
  },
  methods: {
    //获取列表数据(默认当日数据)
    getdata(page, pagesize) {
      this.$http
        .post(this.PATH.SPREADDATALS, {
          page: page,
          pagesize: pagesize
        })
        .then(success => {
          // console.log(success, "列表");
          if (success.status == 200) {
            if (success.data.errno == 0) {
              this.table.data = success.data.data;
              this.table.total = success.data.count;
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
    //分页
    changePage(page) {
      this.table.page = page;
      if (this.is_search) {
        this.getSearch();
      } else {
        this.getdata(page, this.table.pagesize);
      }
    },
    goToDetail(row) {
      console.log("row", row);
      this.$router.push({
        name: "spreadDetail",
        query: {
          id: row.spread_id
        }
      });
    },
    // 获取搜索框的输入值
    getSearch() {
      this.is_search = true;
      this.$http
        .post(this.PATH.SPREADDATASEARCH, {
          page: this.table.page,
          pagesize: this.table.pagesize,
          words: this.searchValue
        })
        .then(success => {
          // console.log(success, "搜索");
          if (success.status == 200) {
            if (success.data.errno == 0) {
              this.table.data = success.data.data;
              this.table.total = success.data.count;
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
    }
  }
};
</script>
<style lang="scss">
#dataOverview {
  height: 100%;
  padding: 20px;
  width: 100%;
  box-sizing: border-box;
  -webkit-box-sizing: border-box;
  .h1 {
    font-size: 22px;
    color: #808080;
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
