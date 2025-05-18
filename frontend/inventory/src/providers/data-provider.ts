import type { CrudFilter, DataProvider } from "@refinedev/core";

const validateFilters = (filters: CrudFilter[]) => {
  console.log(filters);
  const validated = filters.map((filter) => {
    if ("field" in filter && ["id", "sphere", "cylinder"].includes(filter.field)) {
      return { ...filter, value: Number(filter.value) };
    }
    return filter;
  });

  console.log(validated);
  return validated;
};

export const dataProvider = (apiUrl: string): DataProvider => ({
  getList: async ({ resource, pagination, filters, sorters, meta }) => {
    const params = new URLSearchParams();

    const { current = 1, pageSize = 10, mode = "server" } = pagination ?? {};

    if (mode === "server") {
      params.append(
        "range",
        JSON.stringify([(current - 1) * pageSize, current * pageSize])
      );
    }

    if (sorters && sorters.length > 0) {
      params.append(
        "sort",
        JSON.stringify(sorters.map((sorter) => [sorter.field, sorter.order]))
      );
    }

    if (filters && filters.length > 0) {
      params.append("filter", JSON.stringify(validateFilters(filters)));
    }

    const response = await fetch(`${apiUrl}/${resource}?${params.toString()}`);

    if (response.status < 200 || response.status > 299) throw response;

    const data = await response.json();

    const total = Number(response.headers.get("x-total-count"));

    return {
      data,
      total,
    };
  },

  getOne: async ({ resource, id, meta }) => {
    const response = await fetch(`${apiUrl}/${resource}/${id}`);

    if (response.status < 200 || response.status > 299) throw response;

    const data = await response.json();

    return { data };
  },

  create: async ({ resource, variables, meta }) => {
    const response = await fetch(`${apiUrl}/${resource}`, {
      method: "POST",
      body: JSON.stringify(variables),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.status < 200 || response.status > 299) throw response;

    const data = await response.json();

    return { data };
  },

  update: async ({ resource, id, variables, meta }) => {
    const response = await fetch(`${apiUrl}/${resource}/${id}`, {
      method: "PUT",
      body: JSON.stringify(variables),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (response.status < 200 || response.status > 299) throw response;

    const data = await response.json();

    return { data };
  },

  deleteOne: async () => {
    // TODO
    throw new Error("Not implemented");
  },

  getApiUrl: () => {
    return apiUrl;
  },
});
