import { useState } from "react";
import { Button, Confirm, useRecordContext, useDelete } from "react-admin";
import DeleteIcon from "@mui/icons-material/Delete";

export const DeleteWithConfirm = () => {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  const [remove, { isPending }] = useDelete("posts", {
    id: record && record.id,
  });

  const handleClick = () => setOpen(true);
  const handleDialogClose = () => setOpen(false);
  const handleConfirm = () => {
    remove();
    setOpen(false);
  };

  return (
    <>
      <Button
        label="Delete"
        onClick={handleClick}
        startIcon={<DeleteIcon />}
        color="error"
      />
      <Confirm
        isOpen={open}
        loading={isPending}
        title={`Delete item #${record && record.id}`}
        content="Are you sure you want to delete this item?"
        onConfirm={handleConfirm}
        onClose={handleDialogClose}
      />
    </>
  );
};
