<script setup lang="tsx">
import {NButton, NPopconfirm} from 'naive-ui';
import {$t} from "@/locales";
import {useTable, useTableOperate} from '@/hooks/common/table';
import {fetchBatchDeleteAccount, fetchDeleteAccount, fetchGetAccountList} from "@/service/api";
import {useAppStore} from "@/store/modules/app";

const appStore = useAppStore();

const {
  columns,
  columnChecks,
  data,
  getData,
  loading,
  mobilePagination,
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
      key: 'nickName',
      title: $t('page.business.account.nickName'),
      dataIndex: 'nickName',
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
      key: 'activated',
      title: $t('page.business.account.activated'),
      dataIndex: 'activated',
      align: 'center',
      width: 200
    },
    {
      key: 'monitor',
      title: $t('page.business.account.monitor'),
      dataIndex: 'monitor',
      align: 'center',
      width: 200
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
      width: 150
    },

    {
      key: 'operate',
      title: $t('common.operate'),
      align: 'center',
      width: 150,
      render: row => (
        <div class="flex-center gap-8px">
          <NButton type="primary" ghost size="small" onClick={() => edit(row.id)}>
            {$t('common.edit')}
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
</script>

<template>
  <div ref="wrapperRef" class="flex-col-stretch gap-16px overflow-hidden lt-sm:overflow-auto">
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
      <!--      <MenuOperateModal-->
      <!--        v-model:visible="visible"-->
      <!--        :operate-type="operateType"-->
      <!--        :row-data="editingData"-->
      <!--        :all-pages="allPages"-->
      <!--        @submitted="getDataByPage"-->
      <!--      />-->
    </NCard>
  </div>
</template>

<style scoped>

</style>
