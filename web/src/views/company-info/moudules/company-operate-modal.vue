<script setup lang="ts">
import {computed, reactive, ref, watch} from "vue";
import {$t} from "@/locales";
import {statusTypeOptions, userGenderOptions} from "@/constants/business";
import {
  fetchAddLicense,
  fetchAddRole,
  fetchAddUser,
  fetchUpdateLicense,
  fetchUpdateRole,
  fetchUpdateUser
} from "@/service/api";
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

const model: Api.Business.LicenseAddParams = reactive(createDefaultModel());

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
    const {error} = await fetchAddLicense(model);
    if (!error) {
      window.$message?.success($t('common.addSuccess'));
    }
  } else if (props.operateType === 'edit') {
    console.log(model);
    const {error} = await fetchUpdateLicense(model);
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
  <NModal v-model:show="visible" preset="dialog" :title="title" class="min-w-200">
    <NForm
      ref="formRef"
      :model="model"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
      class="max-w-230"
    >
      <NFormItem :label="$t('page.business.license.licenseId')" path="licenseId">
        <NInput
          v-model:value="model.licenseId"
          :placeholder="$t('page.business.license.form.licenseId')"
          :on-update-value="
            (value: string) => {
              model.licenseId = value;
            }
          "
        />
      </NFormItem>
      <NFormItem :label="$t('page.business.license.issuanceTime')" path="password">
        <NInput v-model:value="model.issuanceTime" :placeholder="$t('page.business.license.form.issuanceTime')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.licenseType')" path="nickName">
        <NInput v-model:value="model.licenseType" :placeholder="$t('page.business.license.form.licenseType')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.licenseCategory')" path="userPhone">
        <NInput v-model:value="model.licenseCategory" :placeholder="$t('page.business.license.form.licenseCategory')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.licenseCompany')" path="email">
        <NInput v-model:value="model.licenseCompany" :placeholder="$t('page.business.license.form.licenseCompany')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.taxIdentificationNumber')" path="taxIdentificationNumber">
        <NInput v-model:value="model.taxIdentificationNumber"
                :placeholder="$t('page.business.license.form.taxIdentificationNumber')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.companyAddress')" path="companyAddress">
        <NInput v-model:value="model.companyAddress" :placeholder="$t('page.business.license.form.companyAddress')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.companyName')" path="companyName">
        <NInput v-model:value="model.companyName" :placeholder="$t('page.business.license.form.companyName')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.factoryRegistrationNumber')" path="factoryRegistrationNumber">
        <NInput v-model:value="model.factoryRegistrationNumber"
                :placeholder="$t('page.business.license.form.factoryRegistrationNumber')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.factoryAddress')" path="factoryAddress">
        <NInput v-model:value="model.factoryAddress" :placeholder="$t('page.business.license.form.factoryAddress')"/>
      </NFormItem>
      <NFormItem :label="$t('page.business.license.details')" path="details">
        <NInput v-model:value="model.details"
                type="textarea"
                size="small"
                :autosize="{
                  minRows: 3,
                  maxRows: 5,
                }"
                :placeholder="$t('page.business.license.form.details')"/>
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
