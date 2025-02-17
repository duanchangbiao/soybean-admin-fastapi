<script setup lang="ts">
import {$t} from '@/locales';
import {useNaiveForm} from "@/hooks/common/form";
import {translateOptions} from "@/utils/common";
import {aftTypeOptions, morTypeOptions} from "@/constants/business";
import {onMounted, ref} from "vue";
import {fetchGetDictList} from "@/service/api";

const {formRef, validate, restoreValidation} = useNaiveForm();
defineOptions({
  name: 'MorSearch'
});

interface Emits {
  (e: 'reset'): void;

  (e: 'search'): void;
}

const emit = defineEmits<Emits>();

const model = defineModel<Api.Business.MorParamsList>('model', {required: true});


async function reset() {
  await restoreValidation();
  emit('reset');
}

async function search() {
  await validate();
  emit('search');
}

const DictOptions = ref<CommonType.Option<string>[]>([]);

async function getDictOptions() {
  const {error, data} = await fetchGetDictList({size: 1000, dictType: 'mor5_status', dictStatus: '1'});

  if (!error) {
    const options = data.records.map(item => ({
      label: item.dictName,
      value: item.dictName
    }));
    DictOptions.value = options;
  }
}

onMounted(() => {
  getDictOptions();
});
</script>

<template>
  <NCard :title="$t('common.search')" :bordered="false" size="small" class="card-wrapper">
    <NForm ref="formRef" :model="model" label-placement="left" :label-width="100">
      <NGrid responsive="screen" item-responsive>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.mor.applyNumber')"
                     path="applyNumber" class="pr-24px">
          <NInput v-model:value="model.applyNumber"
                  :placeholder="$t('page.business.mor.form.applyNumber')"/>
        </NFormItemGi>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.mor.accountNumber')" path="username"
                     class="pr-24px">
          <NInput v-model:value="model.accountNumber" :placeholder="$t('page.business.mor.form.accountNumber')"/>
        </NFormItemGi>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.mor.applyStatus')" path="applyStatus"
                     class="pr-24px">
          <NSelect
            v-model:value="model.applyStatus"
            :placeholder="$t('page.business.aft.form.applyStatus')"
            :options="DictOptions"
            filterable
            clearable
          />
        </NFormItemGi>
        <NFormItemGi span="24 s:8 m:4" :label="$t('page.business.mor.remark')"
                     path="applyNumber" class="pr-24px">
          <NInput v-model:value="model.remark"
                  :placeholder="$t('page.business.mor.form.remark')"/>
        </NFormItemGi>
        <NFormItemGi
          span="24 s:12 m:4"
          :label="$t('page.business.mor.morType')"
          path="userGender"
          class="pr-24px"
        >
          <NSelect
            v-model:value="model.morType"
            :placeholder="$t('page.business.mor.form.morType')"
            :options="translateOptions(morTypeOptions)"
            filterable
            clearable
          />
        </NFormItemGi>
        <NFormItemGi span="24 m:4" class="pr-24px">
          <NSpace class="w-full" justify="end">
            <NButton @click="reset">
              <template #icon>
                <icon-ic-round-refresh class="text-icon"/>
              </template>
              {{ $t('common.reset') }}
            </NButton>
            <NButton type="primary" ghost @click="search">
              <template #icon>
                <icon-ic-round-search class="text-icon"/>
              </template>
              {{ $t('common.search') }}
            </NButton>
          </NSpace>
        </NFormItemGi>
      </NGrid>
    </NForm>
  </NCard>
</template>

<style scoped></style>

