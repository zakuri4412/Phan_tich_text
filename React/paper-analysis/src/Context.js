import React, { useState } from "react";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import { styled } from "@mui/material/styles";
import Paper from "@mui/material/Paper";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import CardActionArea from "@mui/material/CardActionArea";
import CardActions from "@mui/material/CardActions";
import Pagination from "@mui/material/Pagination";

function Context({ data }) {
  const articlesPerPage = 5;
  const [currentPage, setCurrentPage] = useState(1);
  const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: "#fff",
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
    ...theme.applyStyles("dark", {
      backgroundColor: "#1A2027",
    }),
  }));

  const openInNewTab = (url) => {
    window.open(url, "_blank", "noopener,noreferrer");
  };

  const handlePageChange = (event, value) => {
    setCurrentPage(value);
  };

  if (!data?.articles || !Array.isArray(data.articles)) {
    return <p>Không có bài báo nào để hiển thị</p>;
  }

  const paginatedArticles = data.articles.slice(
    (currentPage - 1) * articlesPerPage,
    currentPage * articlesPerPage
  );
  const totalPages = Math.ceil(data.articles.length / articlesPerPage);
  return (
    <div>
      <h2>Kết quả API:</h2>
      <Box
        sx={{
          width: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Stack spacing={3}>
          {paginatedArticles.map((d, index) => (
            <div key={index}>
              {d.title === "" || d.description === "" ? null : (
                <Item>
                  <Card sx={{ width: 950 }}>
                    <CardActionArea>
                      <CardContent>
                        <Typography gutterBottom variant="h6" component="div">
                          {d.title}
                        </Typography>
                        <Typography
                          variant="body2"
                          sx={{ color: "text.secondary" }}
                        >
                          {d.description}
                        </Typography>
                        {d.svm_category && (
                          <Box
                            sx={{
                              display: "inline-block",
                              padding: "2px 8px",
                              backgroundColor: "#1976d2",
                              color: "#fff",
                              borderRadius: "12px",
                              fontSize: "0.75rem",
                              fontWeight: "bold",
                              marginTop: 1,
                            }}
                          >
                            {d.svm_category}
                          </Box>
                        )}
                      </CardContent>
                    </CardActionArea>
                    <CardActions>
                      <Button
                        size="small"
                        color="primary"
                        onClick={() => openInNewTab(d.url)}
                      >
                        More
                      </Button>
                    </CardActions>
                  </Card>
                </Item>
              )}
            </div>
          ))}
        </Stack>
        <Box sx={{ display: "flex", justifyContent: "center", marginTop: 3 }}>
          <Pagination
            count={totalPages}
            page={currentPage}
            onChange={handlePageChange}
          />
        </Box>
      </Box>
    </div>
  );
}

export default Context;
