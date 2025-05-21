import { SearchOutlined } from "@ant-design/icons";
import {
  DeleteButton,
  EditButton,
  FilterDropdown,
  getDefaultSortOrder,
  List,
  ShowButton,
  useTable,
} from "@refinedev/antd";
import { getDefaultFilter } from "@refinedev/core";
import { Button, InputNumber, Select, Space, Table, theme, Tooltip } from "antd";

export const LensList = () => {
  const { token } = theme.useToken();

  const { tableProps, sorters, filters, setFilters } = useTable({
    sorters: { initial: [{ field: "id", order: "asc" }] },
    syncWithLocation: false,
  });

  const clearAllFilters = () => {
    setFilters([], "replace");
  };

  console.log(tableProps);

  return (
    <List
      headerButtons={({ defaultButtons }) => (
        <>
          <Button
            type="primary"
            onClick={clearAllFilters}
            disabled={filters.length === 0}
          >
            Reset Filters
          </Button>
          {defaultButtons}
        </>
      )}
    >
      <Table
        {...tableProps}
        rowKey="id"
        pagination={{ ...tableProps.pagination, showSizeChanger: true }}
      >
        <Table.Column
          dataIndex="id"
          title="ID"
          sorter
          defaultSortOrder={getDefaultSortOrder("id", sorters)}
          filterIcon={(filtered) => (
            <SearchOutlined
              style={{
                color: filtered ? token.colorPrimary : undefined,
              }}
            />
          )}
          filterDropdown={(props) => (
            <FilterDropdown {...props}>
              <InputNumber placeholder={"Search ID"} />
            </FilterDropdown>
          )}
          defaultFilteredValue={getDefaultFilter("id", filters, "eq")}
        />
        <Table.Column
          dataIndex="lens_type"
          title="Lens Type"
          sorter
          defaultSortOrder={getDefaultSortOrder("lens_type", sorters)}
          filterDropdown={(props) => (
            <FilterDropdown {...props}>
              <Select style={{ width: "100%" }} placeholder={"Select Lens Type"}>
                <Select.Option value="CR39">CR39</Select.Option>
                <Select.Option value="High Index 1.67">High Index 1.67</Select.Option>
                <Select.Option value="High Index 1.74">High Index 1.74</Select.Option>
                <Select.Option value="Polycarbonate">Polycarbonate</Select.Option>
                <Select.Option value="Trivex">Trivex</Select.Option>
              </Select>
            </FilterDropdown>
          )}
          defaultFilteredValue={getDefaultFilter("lens_type", filters, "eq")}
        />
        <Table.Column
          dataIndex="sphere"
          title="Sphere"
          sorter
          defaultSortOrder={getDefaultSortOrder("sphere", sorters)}
          filterDropdown={(props) => (
            <FilterDropdown {...props}>
              <InputNumber placeholder={"Search Sphere Value"} />
            </FilterDropdown>
          )}
          defaultFilteredValue={getDefaultFilter("sphere", filters, "eq")}
        />
        <Table.Column
          dataIndex="cylinder"
          title="Cylinder"
          sorter
          defaultSortOrder={getDefaultSortOrder("cylinder", sorters)}
          filterDropdown={(props) => (
            <FilterDropdown {...props}>
              <InputNumber placeholder={"Search Cylinder Value"} />
            </FilterDropdown>
          )}
          defaultFilteredValue={getDefaultFilter("cylinder", filters, "eq")}
        />
        <Table.Column
          dataIndex="unit_price"
          title="Unit Price"
          sorter
          defaultSortOrder={getDefaultSortOrder("unit_price", sorters)}
        />
        <Table.Column
          dataIndex="quantity"
          title="Quantity"
          sorter
          defaultSortOrder={getDefaultSortOrder("quantity", sorters)}
        />
        <Table.Column
          dataIndex="storage_limit"
          title="Storage Limit"
          sorter
          defaultSortOrder={getDefaultSortOrder("storage_limit", sorters)}
        />
        <Table.Column
          dataIndex="comment"
          title="Comment"
          key="comment"
          width={"25rem"}
          render={(text: string) => (
            <Tooltip title={text}>
              <div
                style={{
                  overflow: "hidden",
                  textOverflow: "ellipsis",
                  whiteSpace: "nowrap",
                  maxWidth: "25rem",
                }}
              >
                {text}
              </div>
            </Tooltip>
          )}
        />
        <Table.Column
          title="Actions"
          render={(_, record) => (
            <Space>
              <ShowButton hideText size="small" recordItemId={record.id} />
              <EditButton hideText size="small" recordItemId={record.id} />
              <DeleteButton hideText size="small" recordItemId={record.id} />
            </Space>
          )}
        />
      </Table>
    </List>
  );
};
