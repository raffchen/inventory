import { useForm, useSelect, Create } from "@refinedev/antd";

import { Form, Input, Select, InputNumber } from "antd";

export const LensCreate = () => {
  const { formProps, saveButtonProps } = useForm();

  return (
    <Create saveButtonProps={saveButtonProps} title="Create Lens">
      <Form {...formProps} layout="vertical">
        <Form.Item label="ID" name="id" rules={[{ required: true }]}>
          <InputNumber controls={false} style={{ width: "100%" }} />
        </Form.Item>
        <Form.Item label="Lens Type" name="lens_type" rules={[{ required: true }]}>
          <Input />
        </Form.Item>
        <Form.Item label="Sphere" name="sphere" rules={[{ required: true }]}>
          <InputNumber step="0.01" />
        </Form.Item>
        <Form.Item label="Cylinder" name="cylinder" rules={[{ required: true }]}>
          <InputNumber step="0.01" />
        </Form.Item>
        <Form.Item label="Quantity" name="quantity" rules={[{ required: true }]}>
          <InputNumber step="1" />
        </Form.Item>
        <Form.Item label="Unit Price" name="unit_price" rules={[{ required: true }]}>
          <InputNumber prefix="$" step="0.01" />
        </Form.Item>
        <Form.Item label="Storage Limit" name="storage_limit">
          <InputNumber step="1" />
        </Form.Item>
        <Form.Item label="Comment" name="comment">
          <Input.TextArea autoSize={{ minRows: 3, maxRows: 5 }} />
        </Form.Item>
      </Form>
    </Create>
  );
};
