import {
  Datagrid,
  DateField,
  DateTimeInput,
  Edit,
  FunctionField,
  List,
  NumberField,
  NumberInput,
  Show,
  SimpleForm,
  SimpleShowLayout,
  TextField,
  TextInput,
} from "react-admin";
import { CustomEditToolbar } from "./toolbar";

export const LensList = () => (
  <List>
    <Datagrid>
      <TextField source="id" />
      <TextField source="lens_type" />
      <NumberField source="sphere" />
      <NumberField source="cylinder" />
      <NumberField source="unit_price" />
      <NumberField source="quantity" />
      <NumberField source="storage_limit" />
      <FunctionField
        source="comment"
        render={(record) => {
          if (record.comment?.length > 0)
            return (
              record.comment?.slice(0, 30) +
              (record.comment?.length > 30 ? "…" : "")
            );
          else return "";
        }}
      />
      <DateField source="created_at" showTime />
      <DateField source="updated_at" showTime />
    </Datagrid>
  </List>
);

export const LensShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="id" />
      <TextField source="lens_type" />
      <NumberField source="sphere" />
      <NumberField source="cylinder" />
      <NumberField source="unit_price" />
      <NumberField source="quantity" />
      <NumberField source="storage_limit" />
      <TextField source="comment" />
      <DateField source="created_at" showTime />
      <DateField source="updated_at" showTime />
    </SimpleShowLayout>
  </Show>
);

export const LensEdit = () => {
  const transform = (data: any) => ({
    lens_type: data.lens_type,
    sphere: data.sphere,
    cylinder: data.cylinder,
    unit_price: data.unit_price,
    quantity: data.quantity,
    storage_limit: data.storage_limit,
    comment: data.comment,
  });
  return (
    <Edit transform={transform}>
      <SimpleForm toolbar={<CustomEditToolbar />}>
        <TextInput source="id" InputProps={{ disabled: true }} />
        <TextInput source="lens_type" />
        <NumberInput source="sphere" />
        <NumberInput source="cylinder" />
        <NumberInput source="unit_price" />
        <NumberInput source="quantity" />
        <NumberInput source="storage_limit" />
        <TextInput source="comment" multiline />
        <DateTimeInput source="created_at" InputProps={{ disabled: true }} />
        <DateTimeInput source="updated_at" InputProps={{ disabled: true }} />
      </SimpleForm>
    </Edit>
  );
};
