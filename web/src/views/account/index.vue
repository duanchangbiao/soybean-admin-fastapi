<script setup lang="tsx">
import {NButton, NPopconfirm, NTag} from 'naive-ui';
import {$t} from "@/locales";
import {useTable, useTableOperate} from '@/hooks/common/table';
import {
  fetchBatchDeleteAccount,
  fetchDeleteAccount,
  fetchExecuteAccount,
  fetchGetAccountList,
  fetchUpdateAccount
} from "@/service/api";
import {useAppStore} from "@/store/modules/app";
import {AccountDictTypeRecord, statusTypeRecord} from "@/constants/business";
import AccountOperateModal from "@/views/account/modules/account-operate-modal.vue";
import AccountSearch from "@/views/account/modules/account-search.vue"
import {reactive} from "vue";

const appStore = useAppStore();

const {
  columns,
  columnChecks,
  data,
  getData,
  loading,
  getDataByPage,
  mobilePagination,
  resetSearchParams,
  searchParams
} = useTable({
  columns: () => [
    {
      type: 'selection',
      align: 'center',
      width: 48
    },
    {
      key: 'index',
      title: $t('common.index'),
      dataIndex: 'index',
      align: 'center',
      width: 64
    },
    {
      key: 'accountNumber',
      title: $t('page.business.account.accountNumber'),
      dataIndex: 'accountNumber',
      align: 'center',
      width: 100
    },
    {
      key: 'nickname',
      title: $t('page.business.account.nickname'),
      dataIndex: 'nickname',
      align: 'center',
      width: 150
    },
    {
      key: 'password',
      title: $t('page.business.account.password'),
      dataIndex: 'password',
      align: 'center',
      width: 150
    },
    {
      key: 'activate',
      title: $t('page.business.account.activate'),
      dataIndex: 'activate',
      align: 'center',
      width: 100,
      render: row => {
        if (row.activate === null) {
          return null;
        }

        const tagMap: Record<Api.Common.EnableStatus, NaiveUI.ThemeColor> = {
          1: 'success',
          2: 'warning'
        };

        const label = $t(statusTypeRecord[row.activate]);

        return <NTag type={tagMap[row.activate]}>{label}</NTag>;
      }
    },
    {
      key: 'accountMonitorList',
      title: $t('page.business.account.accountMonitorList'),
      dataIndex: 'accountMonitorList',
      align: 'center',
      width: 300,
      render: row => {
        if (row.accountMonitorList === null) {
          return null;
        }
        const labels = row.accountMonitorList.map((accountMonitor, index) => {
          const label = $t(AccountDictTypeRecord[accountMonitor])
          return label
        })
        return labels.map((label, index) => (
          <span>
            <NTag type="info">{label}</NTag>
          </span>
        ));
      }
    },
    {
      key: 'feedback',
      title: $t('page.business.account.feedback'),
      dataIndex: 'feedback',
      align: 'center',
      width: 200
    },
    {
      key: 'remark',
      title: $t('page.business.account.remark'),
      dataIndex: 'remark',
      align: 'center',
      width: 200
    },

    {
      key: 'fmtCtime',
      title: $t('page.business.account.ctime'),
      dataIndex: 'ctime',
      align: 'center',
      width: 120
    },

    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 180,
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            {$t('common.edit')}
          </NButton>
          <NButton type="primary" ghost size="small" onClick={() => execute(row.id,
            row.accountMonitorList, row.accountNumber, row.password, row.createBy, row.updateBy, row.nickname)}>
            {$t('common.execute')}
          </NButton>
          <NPopconfirm onPositiveClick={() => handleDelete(row.id)}>
            {{
              default: () => $t('common.confirmDelete'),
              trigger: () => (
                <NButton type="error" ghost size="small">
                  {$t('common.delete')}
                </NButton>
              )
            }}
          </NPopconfirm>
        </div>
      )
    }
  ],
  apiFn: fetchGetAccountList,
  apiParams: {
    current: 1,
    size: 10,
    accountNumber: null,
    nickname: null,
    activate: null,
    remark: null,
  },
});
const {
  drawerVisible,
  operateType,
  handleEdit,
  handleAdd,
  checkedRowKeys,
  onBatchDeleted,
  editingData,
  onDeleted
  // closeDrawer
} = useTableOperate(data, getData);

async function handleBatchDelete() {
  // request
  const {error} = await fetchBatchDeleteAccount({ids: checkedRowKeys.value});
  if (!error) {
    onBatchDeleted();
  }
}

async function handleDelete(id: number) {
  // request
  const {error} = await fetchDeleteAccount({id});
  if (!error) {
    onDeleted();
  }
}

function edit(id: number) {
  handleEdit(id);
}

async function execute(id: number, accountMonitorList: string[], accountNumber: string, password: string, createBy: string, updateBy: string, nickname: string) {
  const mode = {id, accountMonitorList, accountNumber, password, createBy, updateBy, nickname}
  const {error} = await fetchExecuteAccount(mode)
  if (!error) {
    window.$message.success($t('page.manage.common.executeSuccess'))
  }
}
</script>

<template>
  <div ref="wrapperRef" class="flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
    <AccountSearch v-model:model="searchParams" @reset="resetSearchParams" @search="getData"/>
    <NCard :title="$t('page.manage.menu.title')" :bordered="false" size="small" class="sm:flex-1-hidden card-wrapper">
      <template #header-extra>
        <TableHeaderOperation
          v-model:columns="columnChecks"
          :disabled-delete="checkedRowKeys.length === 0"
          :loading="loading"
          table-id="menu"
          @add="handleAdd"
          @delete="handleBatchDelete"
          @refresh="getData"
        />
      </template>
      <NDataTable
        v-model:checked-row-keys="checkedRowKeys"
        :columns="columns"
        :data="data"
        size="small"
        :flex-height="!appStore.isMobile"
        :scroll-x="1088"
        :loading="loading"
        :row-key="row => row.id"
        remote
        :pagination="mobilePagination"
        class="sm:h-full"
      />
      <AccountOperateModal
        v-model:visible="drawerVisible"
        :operate-type="operateType"
        :row-data="editingData"
        @submitted="getDataByPage"
      />
    </NCard>
  </div>
</template>

<style scoped>

</style>
