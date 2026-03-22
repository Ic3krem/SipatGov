import { useState } from 'react';
import {
  KeyboardAvoidingView,
  Modal,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Switch,
  Text,
  TextInput,
  View,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

import { SipatColors } from '@/constants/theme';
import { REPORT_TYPE_COLORS } from '@/constants/status';
import { useLanguage } from '@/hooks/use-language';
import type { ReportType } from '@/types/models';

// ── Validation schema ────────────────────────────────
const reportSchema = z.object({
  title: z.string().min(1, 'titleRequired'),
  description: z.string().min(1, 'descriptionRequired'),
  report_type: z.enum([
    'concern',
    'feedback',
    'corruption_tip',
    'progress_update',
    'delay_report',
  ] as const),
  is_anonymous: z.boolean(),
});

type ReportFormData = z.infer<typeof reportSchema>;

// ── Report type options ──────────────────────────────
const REPORT_TYPES: ReportType[] = [
  'concern',
  'feedback',
  'corruption_tip',
  'progress_update',
  'delay_report',
];

// ── Props ────────────────────────────────────────────
interface ReportFormProps {
  visible: boolean;
  onClose: () => void;
  onSubmit: (data: ReportFormData) => void;
}

export function ReportForm({ visible, onClose, onSubmit }: ReportFormProps) {
  const { t } = useLanguage();
  const [typePickerOpen, setTypePickerOpen] = useState(false);

  const {
    control,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ReportFormData>({
    resolver: zodResolver(reportSchema),
    defaultValues: {
      title: '',
      description: '',
      report_type: undefined,
      is_anonymous: false,
    },
  });

  const handleClose = () => {
    reset();
    setTypePickerOpen(false);
    onClose();
  };

  const handleFormSubmit = (data: ReportFormData) => {
    onSubmit(data);
    reset();
    setTypePickerOpen(false);
  };

  const getErrorMessage = (errorKey: string | undefined): string | undefined => {
    if (!errorKey) return undefined;
    return t.reports[errorKey] ?? errorKey;
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={handleClose}
    >
      <KeyboardAvoidingView
        style={styles.keyboardView}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        {/* Header */}
        <View style={styles.header}>
          <Pressable onPress={handleClose} hitSlop={8}>
            <MaterialIcons name="close" size={24} color="#FFFFFF" />
          </Pressable>
          <Text style={styles.headerTitle}>{t.reports.submitReport}</Text>
          <View style={{ width: 24 }} />
        </View>

        <ScrollView
          style={styles.scrollView}
          contentContainerStyle={styles.formContent}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}
        >
          {/* Title Field */}
          <View style={styles.fieldGroup}>
            <Text style={styles.fieldLabel}>{t.reports.reportTitle}</Text>
            <Controller
              control={control}
              name="title"
              render={({ field: { onChange, onBlur, value } }) => (
                <TextInput
                  style={[styles.input, errors.title && styles.inputError]}
                  placeholder={t.reports.reportTitlePlaceholder}
                  placeholderTextColor={SipatColors.textMuted}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  maxLength={120}
                />
              )}
            />
            {errors.title && (
              <Text style={styles.errorText}>
                {getErrorMessage(errors.title.message)}
              </Text>
            )}
          </View>

          {/* Description Field */}
          <View style={styles.fieldGroup}>
            <Text style={styles.fieldLabel}>{t.reports.reportDescription}</Text>
            <Controller
              control={control}
              name="description"
              render={({ field: { onChange, onBlur, value } }) => (
                <TextInput
                  style={[
                    styles.input,
                    styles.textArea,
                    errors.description && styles.inputError,
                  ]}
                  placeholder={t.reports.reportDescriptionPlaceholder}
                  placeholderTextColor={SipatColors.textMuted}
                  value={value}
                  onChangeText={onChange}
                  onBlur={onBlur}
                  multiline
                  numberOfLines={5}
                  textAlignVertical="top"
                  maxLength={1000}
                />
              )}
            />
            {errors.description && (
              <Text style={styles.errorText}>
                {getErrorMessage(errors.description.message)}
              </Text>
            )}
          </View>

          {/* Report Type Picker */}
          <View style={styles.fieldGroup}>
            <Text style={styles.fieldLabel}>{t.reports.reportType}</Text>
            <Controller
              control={control}
              name="report_type"
              render={({ field: { onChange, value } }) => (
                <View>
                  <Pressable
                    style={[
                      styles.pickerButton,
                      errors.report_type && styles.inputError,
                    ]}
                    onPress={() => setTypePickerOpen(!typePickerOpen)}
                  >
                    <Text
                      style={[
                        styles.pickerButtonText,
                        !value && styles.placeholderText,
                      ]}
                    >
                      {value ? (t.reports[value] ?? value) : t.reports.selectType}
                    </Text>
                    <MaterialIcons
                      name={typePickerOpen ? 'expand-less' : 'expand-more'}
                      size={20}
                      color={SipatColors.textSecondary}
                    />
                  </Pressable>

                  {typePickerOpen && (
                    <View style={styles.typeOptionsContainer}>
                      {REPORT_TYPES.map((rt) => {
                        const color = REPORT_TYPE_COLORS[rt];
                        const isSelected = value === rt;
                        return (
                          <Pressable
                            key={rt}
                            style={[
                              styles.typeOption,
                              isSelected && {
                                backgroundColor: color + '1A',
                                borderColor: color,
                              },
                            ]}
                            onPress={() => {
                              onChange(rt);
                              setTypePickerOpen(false);
                            }}
                          >
                            <View
                              style={[
                                styles.typeOptionDot,
                                { backgroundColor: color },
                              ]}
                            />
                            <Text
                              style={[
                                styles.typeOptionText,
                                isSelected && { color, fontWeight: '600' },
                              ]}
                            >
                              {t.reports[rt] ?? rt}
                            </Text>
                          </Pressable>
                        );
                      })}
                    </View>
                  )}
                </View>
              )}
            />
            {errors.report_type && (
              <Text style={styles.errorText}>
                {getErrorMessage(errors.report_type.message)}
              </Text>
            )}
          </View>

          {/* Anonymous Toggle */}
          <View style={styles.fieldGroup}>
            <Controller
              control={control}
              name="is_anonymous"
              render={({ field: { onChange, value } }) => (
                <View style={styles.switchRow}>
                  <View style={styles.switchLabelRow}>
                    <MaterialIcons
                      name="visibility-off"
                      size={18}
                      color={SipatColors.textSecondary}
                    />
                    <Text style={styles.switchLabel}>{t.reports.anonymous}</Text>
                  </View>
                  <Switch
                    value={value}
                    onValueChange={onChange}
                    trackColor={{
                      false: '#D1D5DB',
                      true: SipatColors.gold + '80',
                    }}
                    thumbColor={value ? SipatColors.gold : '#F4F3F4'}
                  />
                </View>
              )}
            />
          </View>

          {/* Action Buttons */}
          <View style={styles.actions}>
            <Pressable style={styles.cancelButton} onPress={handleClose}>
              <Text style={styles.cancelButtonText}>{t.reports.cancel}</Text>
            </Pressable>
            <Pressable
              style={styles.submitButton}
              onPress={handleSubmit(handleFormSubmit)}
            >
              <MaterialIcons name="send" size={16} color="#FFFFFF" />
              <Text style={styles.submitButtonText}>{t.reports.submit}</Text>
            </Pressable>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </Modal>
  );
}

const styles = StyleSheet.create({
  keyboardView: {
    flex: 1,
    backgroundColor: SipatColors.dashboardBg,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: SipatColors.navy,
    paddingHorizontal: 20,
    paddingTop: Platform.OS === 'ios' ? 16 : 20,
    paddingBottom: 16,
  },
  headerTitle: {
    fontSize: 17,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  scrollView: {
    flex: 1,
  },
  formContent: {
    padding: 20,
    paddingBottom: 40,
  },
  fieldGroup: {
    marginBottom: 20,
  },
  fieldLabel: {
    fontSize: 14,
    fontWeight: '600',
    color: SipatColors.textPrimary,
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 15,
    color: SipatColors.textPrimary,
  },
  inputError: {
    borderColor: SipatColors.error,
  },
  textArea: {
    minHeight: 120,
    paddingTop: 12,
  },
  errorText: {
    fontSize: 12,
    color: SipatColors.error,
    marginTop: 4,
    marginLeft: 4,
  },
  pickerButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    paddingHorizontal: 14,
    paddingVertical: 12,
  },
  pickerButtonText: {
    fontSize: 15,
    color: SipatColors.textPrimary,
  },
  placeholderText: {
    color: SipatColors.textMuted,
  },
  typeOptionsContainer: {
    marginTop: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    overflow: 'hidden',
  },
  typeOption: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 14,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: SipatColors.cardBorder,
    gap: 10,
    borderWidth: 1,
    borderColor: 'transparent',
  },
  typeOptionDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  typeOptionText: {
    fontSize: 14,
    color: SipatColors.textPrimary,
  },
  switchRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    paddingHorizontal: 14,
    paddingVertical: 10,
  },
  switchLabelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  switchLabel: {
    fontSize: 15,
    color: SipatColors.textPrimary,
  },
  actions: {
    flexDirection: 'row',
    gap: 12,
    marginTop: 8,
  },
  cancelButton: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 14,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: SipatColors.cardBorder,
    backgroundColor: '#FFFFFF',
  },
  cancelButtonText: {
    fontSize: 15,
    fontWeight: '600',
    color: SipatColors.textSecondary,
  },
  submitButton: {
    flex: 2,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    paddingVertical: 14,
    borderRadius: 10,
    backgroundColor: SipatColors.gold,
  },
  submitButtonText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#FFFFFF',
  },
});
