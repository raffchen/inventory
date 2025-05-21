import { useShow } from "@refinedev/core";
import {
  TextField,
  NumberField,
  DateField,
  MarkdownField,
  Show,
} from "@refinedev/antd";

import { Typography } from "antd";

export const LensShow = () => {
  const {
    query: { data, isLoading },
  } = useShow();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <Show isLoading={isLoading} title="Show Lens">
      <Typography.Title level={5}>Id</Typography.Title>
      <TextField value={data?.data?.id} />

      <Typography.Title level={5}>Lens Type</Typography.Title>
      <TextField value={data?.data?.lens_type} />

      <Typography.Title level={5}>Sphere</Typography.Title>
      <NumberField
        value={data?.data?.sphere}
        options={{ minimumSignificantDigits: 3 }}
      />

      <Typography.Title level={5}>Cylinder</Typography.Title>
      <NumberField
        value={data?.data?.cylinder}
        options={{ minimumSignificantDigits: 3 }}
      />

      <Typography.Title level={5}>Quantity</Typography.Title>
      <NumberField value={data?.data?.quantity} />

      <Typography.Title level={5}>Unit Price</Typography.Title>
      <NumberField
        value={data?.data?.unit_price}
        options={{ style: "currency", currency: "USD" }}
      />

      <Typography.Title level={5}>Storage Limit</Typography.Title>
      <NumberField value={data?.data?.storage_limit} />

      <Typography.Title level={5}>Comment</Typography.Title>
      <MarkdownField value={data?.data?.comment} />

      <Typography.Title level={5}>Created At</Typography.Title>
      <DateField value={data?.data?.created_at} format="MM/DD/YYYY hh:mm:ss A" />

      <Typography.Title level={5}>Updated At</Typography.Title>
      <DateField value={data?.data?.updated_at} format="MM/DD/YYYY hh:mm:ss A" />
    </Show>
  );
};
