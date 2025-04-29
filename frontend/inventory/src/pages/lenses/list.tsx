import { useTable, useNavigation } from "@refinedev/core";

import { Link } from "react-router";

export const LensList = () => {
  const {
    tableQuery: { data, isLoading },
    current,
    setCurrent,
    pageCount,
    sorters,
    setSorters,
  } = useTable({
    pagination: { current: 1, pageSize: 10 },
    sorters: { initial: [{ field: "id", order: "asc" }] },
  });

  const { showUrl, editUrl } = useNavigation();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const onPrevious = () => {
    if (current > 1) {
      setCurrent(current - 1);
    }
  };

  const onNext = () => {
    if (current < pageCount) {
      setCurrent(current + 1);
    }
  };

  const onPage = (page: number) => {
    setCurrent(page);
  };

  const getSorter = (field: string) => {
    const sorter = sorters?.find((sorter) => sorter.field === field);

    if (sorter) {
      return sorter.order;
    }
  };

  const onSort = (field: string) => {
    const sorter = getSorter(field);
    setSorters(
      sorter === "desc"
        ? []
        : [
            {
              field,
              order: sorter === "asc" ? "desc" : "asc",
            },
          ]
    );
  };

  const indicator = { asc: "⬆️", desc: "⬇️" };

  return (
    <div>
      <h1>Products</h1>
      <table>
        <thead>
          <tr>
            <th onClick={() => onSort("id")}>ID {indicator[getSorter("id")]}</th>
            <th onClick={() => onSort("lens_type")}>
              Type {indicator[getSorter("lens_type")]}
            </th>
            <th onClick={() => onSort("sphere")}>
              Sphere {indicator[getSorter("sphere")]}
            </th>
            <th onClick={() => onSort("cylinder")}>
              Cylinder {indicator[getSorter("cylinder")]}
            </th>
            <th onClick={() => onSort("unit_price")}>
              Unit Price {indicator[getSorter("unit_price")]}
            </th>
            <th onClick={() => onSort("quantity")}>
              Quantity {indicator[getSorter("quantity")]}
            </th>
            <th onClick={() => onSort("storage_limit")}>
              Storage Limit {indicator[getSorter("storage_limit")]}
            </th>
            <th>Comment</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {data?.data?.map((lens) => (
            <tr key={lens.id}>
              <td>{lens.id}</td>
              <td>{lens.lens_type}</td>
              <td>{lens.sphere}</td>
              <td>{lens.cylinder}</td>
              <td>{lens.unit_price.toFixed(2)}</td>
              <td>{lens.quantity}</td>
              <td>{lens.storage_limit}</td>
              <td>{lens.comment}</td>
              <td>
                <Link to={showUrl("lenses", lens.id)}>Show</Link>
                <Link to={editUrl("lenses", lens.id)}>Edit</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        <button type="button" onClick={onPrevious}>
          {"<"}
        </button>
        <div>
          {current - 1 > 0 && (
            <span onClick={() => onPage(current - 1)}>{current - 1}</span>
          )}
          <span className="current">{current}</span>
          {current + 1 < pageCount && (
            <span onClick={() => onPage(current + 1)}>{current + 1}</span>
          )}
        </div>
        <button type="button" onClick={onNext}>
          {">"}
        </button>
      </div>
    </div>
  );
};
