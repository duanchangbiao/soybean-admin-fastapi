<script setup lang="ts">
import {computed, reactive, ref, watch} from "vue";
import {$t} from "@/locales";
import {statusTypeOptions, userGenderOptions} from "@/constants/business";
import {fetchAddRole, fetchAddUser, fetchUpdateRole, fetchUpdateUser} from "@/service/api";
import {useNaiveForm} from "@/hooks/common/form";

defineOptions({
  name: 'CompanyOperateModal'
});
const visible = defineModel<boolean>('visible', {
  default: false
});

interface Emits {
  (e: 'submitted'): void;
}

interface Props {
  /** the type of operation */
  operateType: NaiveUI.TableOperateType;
  /** the edit row data */
  rowData?: Api.SystemManage.Role | null;
}

const emit = defineEmits<Emits>();

const props = defineProps<Props>();

const model: Api.Business.LicenseUpdateParams = reactive(createDefaultModel());

function createDefaultModel(): Api.Business.LicenseAddParams {
  return {
    companyName: '',
    companyAddress: '',
    factoryAddress: '',
    factoryRegistrationNumber: '',
    issuanceTime: '',
    licenseCategory: '',
    licenseCompany: '',
    licenseId: '',
    licenseType: '',
    taxIdentificationNumber: '',
    details: ''
  };
};


const title = computed(() => {
  const titles: Record<NaiveUI.TableOperateType, string> = {
    add: $t('page.business.license.addLicense'),
    edit: $t('page.business.license.editLicense')
  };
  return titles[props.operateType];
});

// 关闭弹框
function closeDrawer() {
  visible.value = false;
}

// 打开弹框
function handleInitModel() {
  Object.assign(model, createDefaultModel());
  if (props.operateType === 'edit' && props.rowData) {
    console.log('props.rowData', props.rowData);
    Object.assign(model, props.rowData);
  }
}

const {formRef, validate, restoreValidation} = useNaiveForm();

async function handleSubmit() {
  await validate();
  // request

  if (props.operateType === 'add') {
    const {error} = await fetchAddUser(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    console.log(model);
    const {error} = await fetchUpdateUser(model);
    if (!error) {
      window.$message?.success($t('common.updateSuccess'));
    }
  }

  closeDrawer();
  emit('submitted');
}

watch(visible, () => {
  if (visible.value) {
    handleInitModel();
    restoreValidation();
  }
});
</script>

<template>
  <NModal v-model:show="visible" preset="dialog" :title="title" width="800px">
    <NForm
      ref="formRef"
      :model="model"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
      class="max-w-630"
    >
      <NFormItem :label="$t('page.manage.user.userName')" path="userName">
        <NInput
          v-model:value="model.licenseId"
          :placeholder="$t('page.manage.user.form.userName')"
          :on-update-value="
            (value: string) => {
              model.licenseId = value;
            }
          "
        />
      </NFormItem>
      <NFormItem :label="$t('page.manage.user.password')" path="password">
        <NInput v-model:value="model.password" :placeholder="$t('page.manage.user.form.password')"/>
      </NFormItem>
      <NFormItem :label="$t('page.manage.user.nickName')" path="nickName">
        <NInput v-model:value="model.nickName" :placeholder="$t('page.manage.user.form.nickName')"/>
      </NFormItem>
      <NFormItem :label="$t('page.manage.user.userPhone')" path="userPhone">
        <NInput v-model:value="model.userPhone" :placeholder="$t('page.manage.user.form.userPhone')"/>
      </NFormItem>
      <NFormItem :label="$t('page.manage.user.userEmail')" path="email">
        <NInput v-model:value="model.userEmail" :placeholder="$t('page.manage.user.form.userEmail')"/>
      </NFormItem>
      <NFormItem :label="$t('page.manage.user.userRole')" path="roles">
        <NSelect
          v-model:value="model.byUserRoleCodeList"
          multiple
          filterable
          clearable
          :options="roleOptions"
          :placeholder="$t('page.manage.user.form.userRole')"
        />
      </NFormItem>
      <NFormItem :label="$t('page.manage.user.userStatusType')" path="status">
        <NRadioGroup v-model:value="model.statusType">
          <NRadio v-for="item in statusTypeOptions" :key="item.value" :value="item.value" :label="$t(item.label)"/>
        </NRadioGroup>
      </NFormItem>
    </NForm>
    <template #action>
      <NSpace :size="16">
        <NButton @click="closeDrawer">{{ $t('common.cancel') }}</NButton>
        <NButton type="primary" @click="handleSubmit">{{ $t('common.confirm') }}</NButton>
      </NSpace>
    </template>
  </NModal>
</template>

<style scoped>

</style>
